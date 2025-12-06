"""
LangGraph Graph Definition and Compilation

This module creates and compiles the LangGraph with all nodes, edges,
and conditional routing logic.
"""

from typing import Literal, Any

# Import local modules first (to avoid circular import)
from langgraph_service.graph.state import GraphState
from langgraph_service.graph.nodes import (
    classify_query_node,
    retrieve_node,
    format_context_node,
    generate_node,
    direct_answer_node,
    respond_node,
)

# Lazy import StateGraph to avoid circular dependency
# Import it inside functions when needed
def _get_state_graph():
    """Lazy import StateGraph from LangGraph library."""
    try:
        import sys
        import importlib
        import importlib.util
        from pathlib import Path
        
        # Strategy: Find and import the installed langgraph package
        # We need to bypass our local langgraph module
        
        # Save references to our local modules
        modules_to_restore = {}
        for mod_name in list(sys.modules.keys()):
            if mod_name.startswith('langgraph'):
                modules_to_restore[mod_name] = sys.modules[mod_name]
        
        # Remove from cache
        for mod_name in modules_to_restore:
            del sys.modules[mod_name]
        
        try:
            # First, check if we can detect the conflict
            import importlib.util
            spec = importlib.util.find_spec('langgraph')
            if spec and spec.origin:
                spec_path = Path(spec.origin).resolve()
                # Check if it's our local module (not in site-packages)
                is_local = 'site-packages' not in str(spec_path) and 'dist-packages' not in str(spec_path)
                if is_local:
                    # We have a conflict - our local langgraph is being found first
                    # Try to work around it by using the known installed package path
                    import site
                    site_packages = site.getsitepackages()
                    for sp_path in site_packages:
                        installed_graph_path = Path(sp_path) / 'langgraph' / 'graph' / '__init__.py'
                        if installed_graph_path.exists():
                            # We found the installed package, but can't import it normally
                            # This is a known limitation - provide helpful error
                            try:
                                import importlib.metadata
                                version = importlib.metadata.version('langgraph')
                            except:
                                version = "installed"
                            
                            raise ImportError(
                                f"PACKAGE NAME CONFLICT DETECTED\n\n"
                                f"The local 'langgraph' package in this project conflicts with the installed "
                                f"langgraph library (version {version}).\n\n"
                                f"SOLUTION: Rename the local 'langgraph' directory:\n"
                                f"  mv langgraph langgraph_service\n\n"
                                f"Then update all imports from 'langgraph' to 'langgraph_service' in your code.\n"
                                f"Alternatively, use a virtual environment and install langgraph there."
                            )
            
            # Find the installed langgraph package in site-packages
            import site
            site_packages = site.getsitepackages()
            
            # Also check user site-packages
            try:
                user_site = site.getusersitepackages()
                if user_site:
                    site_packages.append(user_site)
            except:
                pass
            
            StateGraph = None
            found_package = False
            
            # Look for langgraph in site-packages
            for sp_path in site_packages:
                langgraph_path = Path(sp_path) / 'langgraph'
                graph_init_path = langgraph_path / 'graph' / '__init__.py'
                
                if not graph_init_path.exists():
                    continue
                
                # Found installed package! Try to load StateGraph
                try:
                    # Method 1: Load module directly from file
                    spec = importlib.util.spec_from_file_location(
                        'langgraph_lib_graph',
                        graph_init_path
                    )
                    if spec and spec.loader:
                        # We need to set up the parent package structure
                        # First, create a minimal langgraph package
                        if 'langgraph_lib' not in sys.modules:
                            langgraph_lib_pkg = importlib.util.module_from_spec(
                                importlib.util.spec_from_file_location(
                                    'langgraph_lib',
                                    langgraph_path / '__init__.py'
                                )
                            )
                            sys.modules['langgraph_lib'] = langgraph_lib_pkg
                        
                        graph_module = importlib.util.module_from_spec(spec)
                        graph_module.__package__ = 'langgraph.graph'
                        graph_module.__name__ = 'langgraph.graph'
                        spec.loader.exec_module(graph_module)
                        
                        if hasattr(graph_module, 'StateGraph'):
                            StateGraph = graph_module.StateGraph
                            found_package = True
                            break
                except Exception:
                    pass
                
                # Method 2: Import by manipulating sys.path and using importlib machinery
                try:
                    # Save current state
                    original_path = sys.path[:]
                    original_cwd = Path.cwd()
                    cwd_str = str(original_cwd)
                    
                    # Create a clean environment for importing
                    # Remove current directory and any parent directories from path
                    paths_to_remove = [cwd_str]
                    for parent in original_cwd.parents:
                        parent_str = str(parent)
                        if parent_str in sys.path:
                            paths_to_remove.append(parent_str)
                    
                    for path_to_remove in paths_to_remove:
                        if path_to_remove in sys.path:
                            sys.path.remove(path_to_remove)
                    
                    # Add site-packages first (before any remaining paths)
                    if str(sp_path) not in sys.path:
                        sys.path.insert(0, str(sp_path))
                    
                    # Clear ALL langgraph modules from cache (including submodules)
                    modules_to_clear = [m for m in list(sys.modules.keys()) if m.startswith('langgraph')]
                    for mod in modules_to_clear:
                        del sys.modules[mod]
                    
                    # Now import - should get installed package since current dir is removed
                    langgraph_pkg = importlib.import_module('langgraph')
                    
                    # Verify it's the installed package by checking __file__
                    pkg_file = getattr(langgraph_pkg, '__file__', None)
                    if pkg_file:
                        pkg_file_str = str(Path(pkg_file).resolve())
                        sp_path_str = str(Path(sp_path).resolve())
                        if sp_path_str not in pkg_file_str:
                            # This is not from the site-packages we're checking, try next
                            continue
                    
                    # Get StateGraph from langgraph_service.graph
                    if hasattr(langgraph_pkg, 'graph'):
                        graph_submodule = langgraph_pkg.graph
                        if hasattr(graph_submodule, 'StateGraph'):
                            StateGraph = graph_submodule.StateGraph
                            found_package = True
                            break
                except Exception as e:
                    # Debug: uncomment to see what's happening
                    # print(f"Import attempt failed: {e}")
                    pass
                finally:
                    # Always restore path
                    sys.path[:] = original_path
                
                if found_package:
                    break
            
            if not found_package or StateGraph is None:
                # Last resort: Try using importlib.machinery to load directly
                try:
                    import importlib.machinery
                    for sp_path in site_packages:
                        graph_init_path = Path(sp_path) / 'langgraph' / 'graph' / '__init__.py'
                        if graph_init_path.exists():
                            # Use SourceFileLoader to load the module
                            loader = importlib.machinery.SourceFileLoader(
                                'langgraph_installed_graph',
                                str(graph_init_path)
                            )
                            # Create a minimal parent package structure
                            if 'langgraph_installed' not in sys.modules:
                                langgraph_init_path = Path(sp_path) / 'langgraph' / '__init__.py'
                                if langgraph_init_path.exists():
                                    parent_loader = importlib.machinery.SourceFileLoader(
                                        'langgraph_installed',
                                        str(langgraph_init_path)
                                    )
                                    parent_module = parent_loader.load_module('langgraph_installed')
                                    sys.modules['langgraph_installed'] = parent_module
                            
                            graph_module = loader.load_module('langgraph_installed_graph')
                            if hasattr(graph_module, 'StateGraph'):
                                StateGraph = graph_module.StateGraph
                                found_package = True
                                break
                except Exception:
                    pass
                
                if not found_package or StateGraph is None:
                    # Check if langgraph is installed at all
                    try:
                        import importlib.metadata
                        try:
                            langgraph_version = importlib.metadata.version('langgraph')
                            # Package is installed, but we can't import it due to local module conflict
                            raise ImportError(
                                f"langgraph package is installed (version {langgraph_version}), but cannot be imported "
                                "due to a conflict with the local 'langgraph' package in this project.\n\n"
                                "SOLUTION: Rename the local 'langgraph' directory to avoid the conflict.\n"
                                "For example: mv langgraph langgraph_service\n\n"
                                "Then update imports in your code to use 'langgraph_service' instead of 'langgraph'."
                            )
                        except importlib.metadata.PackageNotFoundError:
                            # Package is not installed
                            raise ImportError(
                                "langgraph package is not installed. "
                                "Install it with: pip install langgraph"
                            )
                    except ImportError as e:
                        # Re-raise if it's our custom error
                        if "SOLUTION" in str(e):
                            raise
                        # importlib.metadata not available (Python < 3.8), try pkg_resources
                        try:
                            import pkg_resources  # type: ignore
                            pkg_resources.get_distribution('langgraph')
                            # Package is installed but can't import due to conflict
                            raise ImportError(
                                "langgraph package is installed, but cannot be imported "
                                "due to a conflict with the local 'langgraph' package.\n\n"
                                "SOLUTION: Rename the local 'langgraph' directory (e.g., to 'langgraph_service')."
                            )
                        except (pkg_resources.DistributionNotFound, ImportError):
                            # Package not installed
                            raise ImportError(
                                "langgraph package is not installed. "
                                "Install it with: pip install langgraph"
                            )
            
            return StateGraph
            
        finally:
            # Restore our local modules
            for mod_name, module in modules_to_restore.items():
                sys.modules[mod_name] = module
                
    except (ImportError, AttributeError) as e:
        raise ImportError(
            f"Could not import StateGraph from langgraph library: {e}. "
            "Make sure langgraph is installed: pip install langgraph"
        ) from e


def route_after_classification(state: GraphState) -> Literal["rag_path", "direct_path", "respond"]:
    """
    Route decision function after classification.
    
    Determines which path to take based on the query type:
    - rag_required → rag_path (retrieve → format → generate)
    - direct_answer or greeting → direct_path (direct answer)
    - unclear → respond (skip to response)
    
    Args:
        state: Current graph state
        
    Returns:
        Literal string indicating which path to take
    """
    query_type = state.get("metadata", {}).get("query_type", "unclear")
    
    if query_type == "rag_required":
        return "rag_path"
    elif query_type in ["direct_answer", "greeting"]:
        return "direct_path"
    else:  # unclear
        return "respond"


def create_graph() -> Any:  # Using Any to avoid type issues with lazy import
    """
    Create and configure the LangGraph.
    
    This function:
    1. Creates a StateGraph instance
    2. Adds all nodes
    3. Defines edges (connections)
    4. Sets up conditional routing
    
    Returns:
        Configured (but not compiled) StateGraph
    """
    # Lazy import StateGraph
    StateGraph = _get_state_graph()
    
    # Create graph with GraphState
    graph = StateGraph(GraphState)
    
    # Add all nodes
    graph.add_node("classify", classify_query_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("format_context", format_context_node)
    graph.add_node("generate", generate_node)
    graph.add_node("direct_answer", direct_answer_node)
    graph.add_node("respond", respond_node)
    
    # Set entry point
    graph.set_entry_point("classify")
    
    # Add conditional routing after classification
    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {
            "rag_path": "retrieve",
            "direct_path": "direct_answer",
            "respond": "respond"
        }
    )
    
    # RAG path: retrieve → format_context → generate → respond
    graph.add_edge("retrieve", "format_context")
    graph.add_edge("format_context", "generate")
    graph.add_edge("generate", "respond")
    
    # Direct path: direct_answer → respond
    graph.add_edge("direct_answer", "respond")
    
    # Respond is the final node (end)
    graph.set_finish_point("respond")
    
    return graph


def compile_graph() -> Any:  # Using Any to avoid type issues with lazy import
    """
    Create and compile the LangGraph.
    
    Returns:
        Compiled StateGraph ready to use
    """
    graph = create_graph()
    compiled = graph.compile()
    return compiled


# Create a compiled graph instance
# This can be imported and used directly
try:
    app = compile_graph()
except Exception as e:
    # If compilation fails (e.g., LangGraph not installed), set to None
    app = None
    import warnings
    warnings.warn(
        f"Failed to compile LangGraph: {e}. "
        "Make sure langgraph is installed: pip install langgraph"
    )


class RAGGraph:
    """
    Wrapper class for the RAG LangGraph.
    
    Provides a clean interface for using the compiled graph.
    """
    
    def __init__(self):
        """Initialize the RAG graph."""
        self.graph = compile_graph()
    
    def invoke(self, state: GraphState) -> GraphState:
        """
        Invoke the graph with initial state.
        
        Args:
            state: Initial graph state
            
        Returns:
            Final graph state after execution
        """
        return self.graph.invoke(state)
    
    def stream(self, state: GraphState):
        """
        Stream graph execution (yields state after each node).
        
        Args:
            state: Initial graph state
            
        Yields:
            State updates after each node execution
        """
        for state_update in self.graph.stream(state):
            yield state_update


def get_graph() -> Any:  # Using Any to avoid type issues with lazy import
    """
    Get the compiled graph instance.
    
    Returns:
        Compiled StateGraph
    """
    if app is None:
        raise RuntimeError(
            "Graph is not compiled. Make sure langgraph is installed: pip install langgraph"
        )
    return app


#!/usr/bin/env python3
"""
Fix npm permissions and cache issues on macOS.

This script resolves persistent npm permission problems.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def run_command(cmd, shell=False, capture_output=True):
    """Run a command and return result."""
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        else:
            result = subprocess.run(cmd, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def fix_npm_permissions():
    """Fix npm permissions comprehensively."""
    print("🔧 Fixing npm permissions and cache issues...")
    
    home_dir = Path.home()
    npm_dir = home_dir / ".npm"
    npm_config_dir = home_dir / ".npm-config"
    
    # Step 1: Remove problematic cache directory
    print("1️⃣ Removing problematic cache files...")
    problematic_path = npm_dir / "_cacache" / "content-v2" / "sha512" / "fe" / "70"
    if problematic_path.exists():
        try:
            shutil.rmtree(problematic_path)
            print(f"   ✅ Removed {problematic_path}")
        except Exception as e:
            print(f"   ⚠️  Could not remove {problematic_path}: {e}")
    
    # Step 2: Remove entire npm cache
    print("2️⃣ Removing entire npm cache...")
    if npm_dir.exists():
        try:
            shutil.rmtree(npm_dir)
            print("   ✅ Removed ~/.npm directory")
        except Exception as e:
            print(f"   ⚠️  Could not remove ~/.npm: {e}")
    
    # Step 3: Create new npm directory with correct permissions
    print("3️⃣ Creating new npm directory...")
    npm_dir.mkdir(exist_ok=True)
    os.chmod(npm_dir, 0o755)
    
    # Step 4: Set npm to use a different cache directory
    print("4️⃣ Configuring npm to use custom cache...")
    custom_cache = home_dir / ".npm-cache"
    if custom_cache.exists():
        shutil.rmtree(custom_cache)
    custom_cache.mkdir(exist_ok=True)
    os.chmod(custom_cache, 0o755)
    
    # Configure npm to use custom cache
    success, _, _ = run_command(["npm", "config", "set", "cache", str(custom_cache)])
    if success:
        print("   ✅ Set custom npm cache directory")
    else:
        print("   ⚠️  Could not set custom cache directory")
    
    # Step 5: Set npm registry to use https
    print("5️⃣ Configuring npm registry...")
    run_command(["npm", "config", "set", "registry", "https://registry.npmjs.org/"])
    
    # Step 6: Disable optional dependencies by default
    print("6️⃣ Configuring npm settings...")
    run_command(["npm", "config", "set", "optional", "false"])
    run_command(["npm", "config", "set", "fund", "false"])
    run_command(["npm", "config", "set", "audit", "false"])
    
    print("✅ npm permissions and configuration fixed!")


def install_with_yarn():
    """Try installing with yarn as alternative."""
    print("📦 Trying yarn as alternative to npm...")
    
    # Check if yarn is installed
    success, _, _ = run_command(["yarn", "--version"])
    if not success:
        print("   Installing yarn globally...")
        success, _, _ = run_command(["npm", "install", "-g", "yarn"])
        if not success:
            print("   ❌ Could not install yarn")
            return False
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Remove existing lock files
    for lock_file in ["package-lock.json", "yarn.lock"]:
        lock_path = frontend_dir / lock_file
        if lock_path.exists():
            lock_path.unlink()
    
    # Remove node_modules
    node_modules = frontend_dir / "node_modules"
    if node_modules.exists():
        shutil.rmtree(node_modules)
    
    # Install with yarn
    print("   Installing dependencies with yarn...")
    success, stdout, stderr = run_command(["yarn", "install"], capture_output=True)
    
    if success:
        print("   ✅ Dependencies installed with yarn!")
        return True
    else:
        print(f"   ❌ Yarn install failed: {stderr}")
        return False


def create_minimal_package_json():
    """Create a minimal package.json with only essential dependencies."""
    print("📝 Creating minimal package.json...")
    
    frontend_dir = Path(__file__).parent / "frontend"
    
    minimal_package = {
        "name": "rag-chat-frontend",
        "version": "0.1.0",
        "private": True,
        "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "react-scripts": "5.0.1",
            "axios": "^1.4.0"
        },
        "scripts": {
            "start": "react-scripts start",
            "build": "react-scripts build",
            "test": "react-scripts test",
            "eject": "react-scripts eject"
        },
        "eslintConfig": {
            "extends": [
                "react-app",
                "react-app/jest"
            ]
        },
        "browserslist": {
            "production": [
                ">0.2%",
                "not dead",
                "not op_mini all"
            ],
            "development": [
                "last 1 chrome version",
                "last 1 firefox version",
                "last 1 safari version"
            ]
        },
        "proxy": "http://localhost:8000"
    }
    
    import json
    package_path = frontend_dir / "package.json"
    with open(package_path, 'w') as f:
        json.dump(minimal_package, f, indent=2)
    
    print("   ✅ Created minimal package.json")


def try_manual_install():
    """Try manual installation with different approaches."""
    frontend_dir = Path(__file__).parent / "frontend"
    
    print("🔄 Trying manual installation approaches...")
    
    # Approach 1: Use different npm flags
    approaches = [
        ["npm", "install", "--no-package-lock", "--no-optional"],
        ["npm", "install", "--legacy-peer-deps", "--no-package-lock"],
        ["npm", "install", "--force", "--no-package-lock"],
        ["npm", "ci", "--legacy-peer-deps"],
    ]
    
    for i, cmd in enumerate(approaches, 1):
        print(f"   Approach {i}: {' '.join(cmd)}")
        success, stdout, stderr = run_command(cmd, capture_output=True)
        
        if success:
            print(f"   ✅ Success with approach {i}!")
            return True
        else:
            print(f"   ❌ Approach {i} failed")
    
    return False


def main():
    """Main function to fix npm issues."""
    print("🚀 npm Permission Fixer")
    print("=" * 50)
    
    # Step 1: Fix npm permissions
    fix_npm_permissions()
    
    # Step 2: Create minimal package.json
    create_minimal_package_json()
    
    # Step 3: Try different installation methods
    print("\n📦 Attempting to install dependencies...")
    
    # Method 1: Try with fixed npm
    print("\nMethod 1: Fixed npm")
    if try_manual_install():
        print("✅ Dependencies installed successfully with npm!")
        return
    
    # Method 2: Try with yarn
    print("\nMethod 2: Yarn alternative")
    if install_with_yarn():
        print("✅ Dependencies installed successfully with yarn!")
        return
    
    # Method 3: Manual instructions
    print("\nMethod 3: Manual installation required")
    print("=" * 50)
    print("❌ Automatic installation failed. Please try manually:")
    print("")
    print("1. Open Terminal as Administrator/sudo:")
    print("   sudo -i")
    print("")
    print("2. Fix npm permissions:")
    print("   chown -R $(whoami) ~/.npm")
    print("   chmod -R 755 ~/.npm")
    print("")
    print("3. Install dependencies:")
    print(f"   cd {Path(__file__).parent / 'frontend'}")
    print("   npm install --unsafe-perm --allow-root")
    print("")
    print("4. Or use alternative package manager:")
    print("   # Install pnpm")
    print("   npm install -g pnpm")
    print("   pnpm install")
    print("")
    print("5. Or use Docker (if available):")
    print("   docker run -it --rm -v $(pwd):/app -w /app node:18 npm install")


if __name__ == "__main__":
    main()

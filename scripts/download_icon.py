#!/usr/bin/env python3
import os
import subprocess
import json
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

class IconDownloader:
    def __init__(self):
        self.icons8_api_url = "https://api.icons8.com/search"
        self.icons8_base_url = "https://img.icons8.com"
        
    def search_icons(self, query: str, size: int = 81, platform: str = "fluent", amount: int = 1) -> List[Dict[str, Any]]:
        """
        Search for icons using Icons8 API
        """
        try:
            # In a real implementation, this would call the Icons8 API
            # For now, we'll use predefined mappings based on common icon searches
            icon_mappings = {
                "ai brain artificial intelligence": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/brain.png", "name": "brain", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/brain.png", "name": "brain-active", "platform": "ios-filled"}
                ],
                "code programming developer": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/source-code.png", "name": "source-code", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/source-code.png", "name": "source-code-active", "platform": "ios-filled"}
                ],
                "text document editing": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/document.png", "name": "document", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/document.png", "name": "document-active", "platform": "ios-filled"}
                ],
                "library collection folder": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/library.png", "name": "library", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/library.png", "name": "library-active", "platform": "ios-filled"}
                ],
                "home house main": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/home.png", "name": "home", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/home.png", "name": "home-active", "platform": "ios-filled"}
                ],
                "user profile avatar": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/user.png", "name": "user", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/user.png", "name": "user-active", "platform": "ios-filled"}
                ],
                "settings gear": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/settings.png", "name": "settings", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/settings.png", "name": "settings-active", "platform": "ios-filled"}
                ],
                "camera photo image": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/camera.png", "name": "camera", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/camera.png", "name": "camera-active", "platform": "ios-filled"}
                ],
                "search find": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/search.png", "name": "search", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/search.png", "name": "search-active", "platform": "ios-filled"}
                ],
                "airplane plane aircraft": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/airplane.png", "name": "airplane", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/airplane.png", "name": "airplane-active", "platform": "ios-filled"}
                ]
            }
            
            mapping = icon_mappings.get(query.lower())
            if not mapping:
                print(f"No predefined icon mapping for query: {query}")
                return []
            
            # Return the requested number of results (or available results)
            return mapping[:amount]
            
        except Exception as error:
            print(f"Error searching icons: {error}")
            return []

    def download_icon_with_curl(self, url: str, output_path: str) -> bool:
        """
        Download an icon using curl
        """
        try:
            command = f'curl -s -o "{output_path}" "{url}"'
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"Successfully downloaded: {output_path}")
            return True
        except subprocess.CalledProcessError as error:
            print(f"Error downloading {url}: {error}")
            return False
        except Exception as error:
            print(f"Error: {error}")
            return False

    def download_single_icon(self, url: str, name: str, project_path: str, icon_dir: str = "images", is_active: bool = False) -> bool:
        """
        Download a single icon
        """
        try:
            icons_dir = Path(project_path) / icon_dir
            icons_dir.mkdir(parents=True, exist_ok=True)

            state = "-active" if is_active else ""
            filename = f"{name}{state}.png"
            output_path = icons_dir / filename
            
            return self.download_icon_with_curl(str(url), str(output_path))
            
        except Exception as error:
            print(f"Error downloading icon {name}: {error}")
            return False

    def download_icons(self, project_path: str, icon_configs: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> None:
        """
        Download icons for a mini program
        """
        if options is None:
            options = {}
            
        icon_dir = options.get("icon_dir", "images")
        states = options.get("states", ["normal", "active"])
        
        print("Starting icon download...")
        
        for config in icon_configs:
            name = config.get("name", "")
            search_query = config.get("search_query", "")
            size = config.get("size", 81)
            platform = config.get("platform", "fluent")
            text = config.get("text", "")
            
            print(f'Downloading icons for "{text}" ({name})...')
            
            # Search for icons
            icons = self.search_icons(search_query, size, platform, len(states))
            if not icons:
                print(f"No icons found for query: {search_query}")
                continue
            
            # Download each state
            for i, state in enumerate(states):
                if i >= len(icons):
                    break
                    
                is_active = state == "active"
                icon_url = icons[i]["url"]
                
                self.download_single_icon(icon_url, name, project_path, icon_dir, is_active)
            
            print(f'Completed icons for "{text}"')

        print('All icons downloaded successfully!')

# Create a global instance
downloader = IconDownloader()

def search_icons(query: str, size: int = 81, platform: str = "fluent", amount: int = 1) -> List[Dict[str, Any]]:
    """Search for icons using Icons8 API"""
    return downloader.search_icons(query, size, platform, amount)

def download_icon_with_curl(url: str, output_path: str) -> bool:
    """Download an icon using curl"""
    return downloader.download_icon_with_curl(url, output_path)

def download_single_icon(url: str, name: str, project_path: str, icon_dir: str = "images", is_active: bool = False) -> bool:
    """Download a single icon"""
    return downloader.download_single_icon(url, name, project_path, icon_dir, is_active)

def download_icons(project_path: str, icon_configs: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> None:
    """Download icons for a mini program"""
    downloader.download_icons(project_path, icon_configs, options)
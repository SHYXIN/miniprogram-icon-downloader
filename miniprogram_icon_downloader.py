#!/usr/bin/env python3
import os
import subprocess
import json
import requests
from pathlib import Path
from typing import List, Dict, Any, Optional

class MiniProgramIconDownloader:
    def __init__(self):
        self.icons8_api_url = "https://api.icons8.com/search"
        self.icons8_base_url = "https://img.icons8.com"
        
    def search_icons(self, query: str, size: int = 81, platform: str = "ios", amount: int = 1) -> List[Dict[str, Any]]:
        """
        Search for icons using Icons8 API with local fallback
        """
        try:
            # Icons8 API endpoint
            api_url = "https://api.icons8.com/search"
            
            # Prepare parameters
            params = {
                'query': query,
                'platform': platform,
                'amount': amount
            }
            
            print(f"Searching for icons: query='{query}', platform='{platform}', amount={amount}")
            
            # Make API request
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            
            # Parse response
            icons = response.json()
            print(f"Found {len(icons)} icons via Icons8 API")
            return icons
            
        except Exception as error:
            print(f"Error searching icons via API: {error}")
            print("Falling back to local icon mappings...")
            
            # Fallback to local icon mappings
            icon_mappings = {
                "girl": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/girl.png", "name": "girl", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/girl.png", "name": "girl-active", "platform": "ios-filled"}
                ],
                "female": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/female.png", "name": "female", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/female.png", "name": "female-active", "platform": "ios-filled"}
                ],
                "woman": [
                    {"url": "https://img.icons8.com/ios/100/8C8C8C/woman.png", "name": "woman", "platform": "ios"},
                    {"url": "https://img.icons8.com/ios-filled/100/1E3A5F/woman.png", "name": "woman-active", "platform": "ios-filled"}
                ]
            }
            
            mapping = icon_mappings.get(query.lower())
            if not mapping:
                print(f"No predefined icon mapping for query: {query}")
                return []
                
            print(f"Found {len(mapping)} icons via local fallback")
            return mapping[:amount]
            
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
        Download icons for mini program
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
            platform = config.get("platform", "ios")
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
downloader = MiniProgramIconDownloader()

def search_icons(query: str, size: int = 81, platform: str = "ios", amount: int = 1) -> List[Dict[str, Any]]:
    """Search for icons using Icons8 API"""
    return downloader.search_icons(query, size, platform, amount)

def download_icon_with_curl(url: str, output_path: str) -> bool:
    """Download an icon using curl"""
    return downloader.download_icon_with_curl(url, output_path)

def download_single_icon(url: str, name: str, project_path: str, icon_dir: str = "images", is_active: bool = False) -> bool:
    """Download a single icon"""
    return downloader.download_single_icon(url, name, project_path, icon_dir, is_active)

def download_icons(project_path: str, icon_configs: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> None:
    """Download icons for mini program"""
    downloader.download_icons(project_path, icon_configs, options)
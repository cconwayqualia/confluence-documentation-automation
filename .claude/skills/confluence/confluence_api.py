#!/usr/bin/env python3
"""
Confluence API Client for Claude Code Skills

Simple API client that reads credentials from config.json
"""

import os
import sys
import json
import argparse
from base64 import b64encode
from typing import Optional, Dict, Any
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


class ConfluenceAPI:
    """Confluence Cloud REST API client"""

    def __init__(self):
        """Initialize the API client with credentials from config.json"""
        # Find config.json in the same directory as this script
        script_dir = Path(__file__).parent
        config_path = script_dir / 'config.json'

        if not config_path.exists():
            raise FileNotFoundError(
                f"Config file not found at {config_path}\n"
                f"Copy config.json.example to config.json and add your credentials"
            )

        # Load config
        with open(config_path, 'r') as f:
            config = json.load(f)

        self.base_url = config.get('confluence_url', '').rstrip('/')
        self.email = config.get('email', '')
        self.api_token = config.get('api_token', '')
        self.space_key = config.get('space_key', '')

        # Validate required fields
        missing = []
        if not self.base_url:
            missing.append('confluence_url')
        if not self.email:
            missing.append('email')
        if not self.api_token:
            missing.append('api_token')
        if not self.space_key:
            missing.append('space_key')

        if missing:
            raise ValueError(
                f"Missing required fields in config.json: {', '.join(missing)}"
            )

        # Clean up base URL (remove trailing slashes, ensure /wiki is present if needed)
        self.base_url = self.base_url.rstrip('/')
        if not self.base_url.endswith('/wiki'):
            # Check if it's just the domain
            if 'atlassian.net' in self.base_url and '/wiki' not in self.base_url:
                self.base_url += '/wiki'

        # Construct API base URL
        self.api_url = f"{self.base_url}/rest/api/content"

        # Set up authentication headers
        self.headers = self._get_auth_headers()

    def _get_auth_headers(self) -> Dict[str, str]:
        """Generate Basic Auth headers for Confluence API"""
        credentials = f"{self.email}:{self.api_token}"
        encoded = b64encode(credentials.encode()).decode()
        return {
            'Authorization': f'Basic {encoded}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def test_connection(self) -> bool:
        """Test API connectivity and authentication"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/api/space",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                print("Connection successful")
                print(f"Connected to: {self.base_url}")
                print(f"Authenticated as: {self.email}")
                return True
            elif response.status_code == 401:
                print("Error: Authentication failed", file=sys.stderr)
                print("Check CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN", file=sys.stderr)
                return False
            elif response.status_code == 403:
                print("Error: Permission denied", file=sys.stderr)
                print("Verify you have access to the Confluence instance", file=sys.stderr)
                return False
            elif response.status_code == 404:
                print("Error: Confluence instance not found", file=sys.stderr)
                print(f"Check CONFLUENCE_URL: {self.base_url}", file=sys.stderr)
                return False
            else:
                print(f"Error: Unexpected status code {response.status_code}", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return False

        except requests.exceptions.Timeout:
            print("Error: Connection timed out", file=sys.stderr)
            print("Check your network connection and Confluence URL", file=sys.stderr)
            return False
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to Confluence", file=sys.stderr)
            print(f"Check CONFLUENCE_URL: {self.base_url}", file=sys.stderr)
            print("Verify you have internet connectivity", file=sys.stderr)
            return False
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return False

    def verify_space(self) -> bool:
        """Verify that the configured space exists and is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/rest/api/space/{self.space_key}",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                space_data = response.json()
                print("Space verified successfully")
                print(f"Space Name: {space_data.get('name', 'N/A')}")
                print(f"Space Key: {self.space_key}")
                return True
            elif response.status_code == 404:
                print(f"Error: Space '{self.space_key}' not found", file=sys.stderr)
                print("Check CONFLUENCE_SPACE_KEY environment variable", file=sys.stderr)
                return False
            elif response.status_code == 403:
                print(f"Error: No permission to access space '{self.space_key}'", file=sys.stderr)
                print("Request access from your Confluence administrator", file=sys.stderr)
                return False
            else:
                print(f"Error: Unexpected status code {response.status_code}", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return False

        except Exception as e:
            print(f"Error verifying space: {str(e)}", file=sys.stderr)
            return False

    def create_space(self, space_key: str, space_name: str, description: str = '') -> bool:
        """
        Create a new Confluence space

        Args:
            space_key: Space key (uppercase, no spaces)
            space_name: Space name (display name)
            description: Optional space description

        Returns:
            True if successful, False otherwise
        """
        payload = {
            'key': space_key,
            'name': space_name,
            'description': {
                'plain': {
                    'value': description or f'Space for {space_name}',
                    'representation': 'plain'
                }
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/rest/api/space",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 201]:
                print("Space created successfully")
                print(f"Space Key: {space_key}")
                print(f"Space Name: {space_name}")
                return True
            elif response.status_code == 400:
                print("Error: Invalid space data", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return False
            elif response.status_code == 401:
                print("Error: Authentication failed", file=sys.stderr)
                return False
            elif response.status_code == 403:
                print("Error: No permission to create spaces", file=sys.stderr)
                print("You need Confluence admin permissions to create spaces", file=sys.stderr)
                return False
            elif response.status_code == 409:
                print(f"Error: Space '{space_key}' already exists", file=sys.stderr)
                return False
            else:
                print(f"Error: Failed to create space (status {response.status_code})", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return False

        except Exception as e:
            print(f"Error creating space: {str(e)}", file=sys.stderr)
            return False

    def create_page(
        self,
        title: str,
        content: str,
        space: str,
        parent_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new Confluence page

        Args:
            title: Page title
            content: Page content in Confluence Storage Format (HTML/XML)
            space: Space key
            parent_id: Optional parent page ID for hierarchy

        Returns:
            Dict with page_id, title, and url, or None if failed
        """
        payload = {
            'type': 'page',
            'title': title,
            'space': {'key': space},
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }
        }

        if parent_id:
            payload['ancestors'] = [{'id': parent_id}]

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 201]:
                data = response.json()
                page_id = data['id']
                web_ui = data.get('_links', {}).get('webui', '')
                page_url = f"{self.base_url}{web_ui}" if web_ui else f"{self.base_url}/pages/viewpage.action?pageId={page_id}"

                print("Page created successfully")
                print(f"Page ID: {page_id}")
                print(f"Page URL: {page_url}")

                return {
                    'page_id': page_id,
                    'title': data['title'],
                    'url': page_url,
                    'version': data['version']['number']
                }

            elif response.status_code == 400:
                print("Error: Invalid page data", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None
            elif response.status_code == 401:
                print("Error: Authentication failed", file=sys.stderr)
                return None
            elif response.status_code == 403:
                print(f"Error: No permission to create pages in space '{space}'", file=sys.stderr)
                return None
            elif response.status_code == 404:
                if parent_id:
                    print(f"Error: Parent page '{parent_id}' not found", file=sys.stderr)
                else:
                    print(f"Error: Space '{space}' not found", file=sys.stderr)
                return None
            else:
                print(f"Error: Failed to create page (status {response.status_code})", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None

        except Exception as e:
            print(f"Error creating page: {str(e)}", file=sys.stderr)
            return None

    def update_page(
        self,
        page_id: str,
        title: str,
        content: str,
        version: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update an existing Confluence page

        Args:
            page_id: The page ID to update
            title: Updated page title
            content: Updated content in Confluence Storage Format
            version: Current version number (if not provided, will fetch)

        Returns:
            Dict with page_id, title, url, and new version, or None if failed
        """
        # If version not provided, fetch current version
        if version is None:
            page_data = self.get_page(page_id)
            if not page_data:
                print("Error: Could not fetch current page version", file=sys.stderr)
                return None
            version = page_data['version']['number']

        payload = {
            'type': 'page',
            'title': title,
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            },
            'version': {
                'number': version + 1
            }
        }

        try:
            response = requests.put(
                f"{self.api_url}/{page_id}",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 204]:
                data = response.json()
                page_id = data['id']
                web_ui = data.get('_links', {}).get('webui', '')
                page_url = f"{self.base_url}{web_ui}" if web_ui else f"{self.base_url}/pages/viewpage.action?pageId={page_id}"

                print("Page updated successfully")
                print(f"Page ID: {page_id}")
                print(f"New Version: {data['version']['number']}")
                print(f"Page URL: {page_url}")

                return {
                    'page_id': page_id,
                    'title': data['title'],
                    'url': page_url,
                    'version': data['version']['number']
                }

            elif response.status_code == 400:
                print("Error: Invalid page data", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None
            elif response.status_code == 404:
                print(f"Error: Page '{page_id}' not found", file=sys.stderr)
                return None
            elif response.status_code == 409:
                print("Error: Version conflict - page was modified by someone else", file=sys.stderr)
                print("Fetch the latest version and try again", file=sys.stderr)
                return None
            else:
                print(f"Error: Failed to update page (status {response.status_code})", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None

        except Exception as e:
            print(f"Error updating page: {str(e)}", file=sys.stderr)
            return None

    def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Get page metadata and content

        Args:
            page_id: The page ID

        Returns:
            Dict with page data, or None if failed
        """
        try:
            response = requests.get(
                f"{self.api_url}/{page_id}?expand=body.storage,version",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"Error: Page '{page_id}' not found", file=sys.stderr)
                return None
            else:
                print(f"Error: Failed to get page (status {response.status_code})", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None

        except Exception as e:
            print(f"Error getting page: {str(e)}", file=sys.stderr)
            return None

    def search_page(self, title: str, space: str) -> Optional[Dict[str, Any]]:
        """
        Search for a page by title in a space

        Args:
            title: Page title to search for
            space: Space key

        Returns:
            Dict with page data if found, None otherwise
        """
        try:
            # Use CQL (Confluence Query Language) to search
            cql = f'type=page AND space="{space}" AND title="{title}"'
            response = requests.get(
                f"{self.base_url}/rest/api/content/search",
                headers=self.headers,
                params={'cql': cql},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])

                if results:
                    page = results[0]  # Take first result
                    print("Page found")
                    print(f"Page ID: {page['id']}")
                    print(f"Page Title: {page['title']}")
                    return page
                else:
                    print(f"No page found with title '{title}' in space '{space}'")
                    return None
            else:
                print(f"Error: Search failed (status {response.status_code})", file=sys.stderr)
                print(response.text, file=sys.stderr)
                return None

        except Exception as e:
            print(f"Error searching for page: {str(e)}", file=sys.stderr)
            return None


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Confluence API Client')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # test-connection command
    subparsers.add_parser('test-connection', help='Test API connectivity and authentication')

    # verify-space command
    subparsers.add_parser('verify-space', help='Verify space exists and is accessible')

    # create-space command
    create_space_parser = subparsers.add_parser('create-space', help='Create a new Confluence space')
    create_space_parser.add_argument('--key', required=True, help='Space key (uppercase, no spaces)')
    create_space_parser.add_argument('--name', required=True, help='Space name (display name)')
    create_space_parser.add_argument('--description', help='Space description (optional)')

    # create-page command
    create_parser = subparsers.add_parser('create-page', help='Create a new page')
    create_parser.add_argument('--title', required=True, help='Page title')
    create_parser.add_argument('--content', help='Page content (HTML)')
    create_parser.add_argument('--content-file', help='File containing page content')
    create_parser.add_argument('--content-stdin', action='store_true', help='Read content from stdin')
    create_parser.add_argument('--space', required=True, help='Space key')
    create_parser.add_argument('--parent-id', help='Parent page ID (for hierarchical pages)')

    # update-page command
    update_parser = subparsers.add_parser('update-page', help='Update an existing page')
    update_parser.add_argument('--page-id', required=True, help='Page ID to update')
    update_parser.add_argument('--title', required=True, help='Updated page title')
    update_parser.add_argument('--content', help='Updated content (HTML)')
    update_parser.add_argument('--content-file', help='File containing updated content')
    update_parser.add_argument('--content-stdin', action='store_true', help='Read content from stdin')
    update_parser.add_argument('--version', type=int, help='Current version number (optional)')

    # get-page command
    get_parser = subparsers.add_parser('get-page', help='Get page metadata')
    get_parser.add_argument('--page-id', required=True, help='Page ID')

    # search-page command
    search_parser = subparsers.add_parser('search-page', help='Search for a page by title')
    search_parser.add_argument('--title', required=True, help='Page title to search for')
    search_parser.add_argument('--space', required=True, help='Space key')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        api = ConfluenceAPI()
    except EnvironmentError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error initializing API client: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Execute command
    if args.command == 'test-connection':
        success = api.test_connection()
        sys.exit(0 if success else 1)

    elif args.command == 'verify-space':
        success = api.verify_space()
        sys.exit(0 if success else 1)

    elif args.command == 'create-space':
        success = api.create_space(args.key, args.name, args.description or '')
        sys.exit(0 if success else 1)

    elif args.command == 'create-page':
        # Get content from one of three sources
        if args.content:
            content = args.content
        elif args.content_file:
            try:
                with open(args.content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading content file: {str(e)}", file=sys.stderr)
                sys.exit(1)
        elif args.content_stdin:
            content = sys.stdin.read()
        else:
            print("Error: Must provide --content, --content-file, or --content-stdin", file=sys.stderr)
            sys.exit(1)

        result = api.create_page(args.title, content, args.space, args.parent_id)
        sys.exit(0 if result else 1)

    elif args.command == 'update-page':
        # Get content from one of three sources
        if args.content:
            content = args.content
        elif args.content_file:
            try:
                with open(args.content_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading content file: {str(e)}", file=sys.stderr)
                sys.exit(1)
        elif args.content_stdin:
            content = sys.stdin.read()
        else:
            print("Error: Must provide --content, --content-file, or --content-stdin", file=sys.stderr)
            sys.exit(1)

        result = api.update_page(args.page_id, args.title, content, args.version)
        sys.exit(0 if result else 1)

    elif args.command == 'get-page':
        result = api.get_page(args.page_id)
        if result:
            print(json.dumps(result, indent=2))
            sys.exit(0)
        else:
            sys.exit(1)

    elif args.command == 'search-page':
        result = api.search_page(args.title, args.space)
        if result:
            print(json.dumps(result, indent=2))
            sys.exit(0)
        else:
            sys.exit(1)

    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

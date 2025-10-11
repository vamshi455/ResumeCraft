"""
Template Management System
Handles template storage, retrieval, and metadata management
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class TemplateManager:
    """Manages resume templates storage and retrieval"""

    def __init__(self, storage_path: str = None):
        """
        Initialize the template manager

        Args:
            storage_path: Path to store templates. Defaults to ./data/templates
        """
        if storage_path is None:
            storage_path = Path(__file__).parent.parent.parent / "data" / "templates"

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.storage_path / "metadata.json"
        self._load_metadata()

    def _load_metadata(self):
        """Load templates metadata from disk"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "templates": {},
                "active_template": None
            }
            self._save_metadata()

    def _save_metadata(self):
        """Save templates metadata to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, indent=2, fp=f)

    def _generate_template_id(self, name: str) -> str:
        """Generate unique template ID"""
        timestamp = datetime.now().isoformat()
        unique_string = f"{name}_{timestamp}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]

    def save_template(
        self,
        name: str,
        file_content: bytes,
        file_extension: str,
        description: str = "",
        set_as_active: bool = True
    ) -> Dict[str, Any]:
        """
        Save a new template

        Args:
            name: Template name
            file_content: Raw file content
            file_extension: File extension (pdf, docx, txt)
            description: Optional template description
            set_as_active: Whether to set this as the active template

        Returns:
            Template metadata dictionary
        """
        # Generate template ID
        template_id = self._generate_template_id(name)

        # Save file
        file_path = self.storage_path / f"{template_id}.{file_extension}"
        with open(file_path, 'wb') as f:
            f.write(file_content)

        # Create metadata
        template_meta = {
            "id": template_id,
            "name": name,
            "description": description,
            "file_path": str(file_path),
            "file_extension": file_extension,
            "file_size": len(file_content),
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "usage_count": 0
        }

        # Store metadata
        self.metadata["templates"][template_id] = template_meta

        # Set as active if requested
        if set_as_active:
            self.metadata["active_template"] = template_id

        self._save_metadata()

        return template_meta

    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get template metadata by ID

        Args:
            template_id: Template ID

        Returns:
            Template metadata or None if not found
        """
        return self.metadata["templates"].get(template_id)

    def get_active_template(self) -> Optional[Dict[str, Any]]:
        """
        Get the currently active template

        Returns:
            Active template metadata or None
        """
        active_id = self.metadata.get("active_template")
        if active_id:
            return self.get_template(active_id)
        return None

    def set_active_template(self, template_id: str) -> bool:
        """
        Set a template as active

        Args:
            template_id: Template ID to activate

        Returns:
            True if successful, False if template not found
        """
        if template_id in self.metadata["templates"]:
            self.metadata["active_template"] = template_id
            self._save_metadata()
            return True
        return False

    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all templates

        Returns:
            List of template metadata dictionaries
        """
        return list(self.metadata["templates"].values())

    def delete_template(self, template_id: str) -> bool:
        """
        Delete a template

        Args:
            template_id: Template ID to delete

        Returns:
            True if successful, False if template not found
        """
        if template_id not in self.metadata["templates"]:
            return False

        template = self.metadata["templates"][template_id]

        # Delete file
        file_path = Path(template["file_path"])
        if file_path.exists():
            file_path.unlink()

        # Remove from metadata
        del self.metadata["templates"][template_id]

        # Clear active template if this was it
        if self.metadata["active_template"] == template_id:
            self.metadata["active_template"] = None

        self._save_metadata()
        return True

    def increment_usage(self, template_id: str):
        """
        Increment template usage counter

        Args:
            template_id: Template ID
        """
        if template_id in self.metadata["templates"]:
            self.metadata["templates"][template_id]["usage_count"] += 1
            self.metadata["templates"][template_id]["last_used"] = datetime.now().isoformat()
            self._save_metadata()

    def read_template_content(self, template_id: str) -> Optional[bytes]:
        """
        Read template file content

        Args:
            template_id: Template ID

        Returns:
            File content as bytes or None if not found
        """
        template = self.get_template(template_id)
        if not template:
            return None

        file_path = Path(template["file_path"])
        if not file_path.exists():
            return None

        with open(file_path, 'rb') as f:
            return f.read()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about templates

        Returns:
            Statistics dictionary
        """
        templates = self.list_templates()

        total_size = sum(t["file_size"] for t in templates)
        total_usage = sum(t["usage_count"] for t in templates)

        return {
            "total_templates": len(templates),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "total_usage": total_usage,
            "active_template": self.metadata.get("active_template"),
            "has_active_template": self.metadata.get("active_template") is not None
        }


# Singleton instance
_template_manager = None


def get_template_manager() -> TemplateManager:
    """Get or create the global template manager instance"""
    global _template_manager
    if _template_manager is None:
        _template_manager = TemplateManager()
    return _template_manager

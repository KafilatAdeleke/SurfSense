"""Add ZENDESK_CONNECTOR to connector enum and document type enum

Revision ID: 10_add_zendesk_connector_enum_and_documenttype
Revises:
00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '10_add_zendesk_connector_enum_and_documenttype'
down_revision = '9_add_discord_connector_enum_and_documenttype'
branch_labels = None
depends_on = None

CONNECTOR_ENUM = "connectortypeenum"
DOCUMENT_ENUM = "documenttypeenum"

def upgrade():
    # Add ZENDESK_CONNECTOR to connector enum
    op.execute("ALTER TYPE connectortypeenum ADD VALUE 'ZENDESK_CONNECTOR'")
    
    # Add ZENDESK_CONNECTOR to document enum  
    op.execute("ALTER TYPE documenttypeenum ADD VALUE 'ZENDESK_CONNECTOR'")

def downgrade():
    # Delete all ZENDESK_CONNECTOR documents
    op.execute("DELETE FROM documents WHERE document_type = 'ZENDESK_CONNECTOR'")
    
    # Delete all ZENDESK_CONNECTOR connectors
    op.execute("DELETE FROM search_source_connectors WHERE connector_type = 'ZENDESK_CONNECTOR'")
    
    # Recreate enums without ZENDESK_CONNECTOR
    # Note: This is a simplified version - production should handle this more carefully
    pass

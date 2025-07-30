"""
Zendesk Connector for fetching tickets and knowledge base articles
"""
import asyncio
from typing import List, Dict, Any, Optional
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket, Article
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ZendeskConnector:
    def __init__(self, subdomain: str, email: str, api_token: str):
        """
        Initialize Zendesk connector
        
        Args:
            subdomain: Zendesk subdomain (e.g., 'company' for company.zendesk.com)
            email: Admin email for authentication
            api_token: API token for authentication
        """
        self.subdomain = subdomain
        self.email = email
        self.api_token = api_token
        
        # Initialize Zenpy client
        creds = {
            'email': email,
            'token': api_token,
            'subdomain': subdomain
        }
        self.client = Zenpy(**creds)
        
    async def get_tickets(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Fetch tickets from Zendesk
        
        Args:
            limit: Maximum number of tickets to fetch
            
        Returns:
            List of ticket dictionaries
        """
        tickets = []
        try:
            # Use search_export for large datasets to avoid 1000 result limit
            ticket_generator = self.client.search_export(type='ticket', status_less_than='closed')
            
            count = 0
            for ticket in ticket_generator:
                if count >= limit:
                    break
                    
                # Get ticket comments
                comments = []
                try:
                    for comment in self.client.tickets.comments(ticket.id):
                        if comment.body and comment.body.strip():
                            comments.append({
                                'author': comment.author_id,
                                'body': comment.body,
                                'created_at': comment.created_at.isoformat() if comment.created_at else None,
                                'public': comment.public
                            })
                except Exception as e:
                    logger.warning(f"Could not fetch comments for ticket {ticket.id}: {e}")
                
                ticket_data = {
                    'id': ticket.id,
                    'subject': ticket.subject or '',
                    'description': ticket.description or '',
                    'status': ticket.status,
                    'priority': ticket.priority,
                    'requester_id': ticket.requester_id,
                    'assignee_id': ticket.assignee_id,
                    'group_id': ticket.group_id,
                    'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
                    'updated_at': ticket.updated_at.isoformat() if ticket.updated_at else None,
                    'tags': ticket.tags or [],
                    'comments': comments,
                    'url': f"https://{self.subdomain}.zendesk.com/agent/tickets/{ticket.id}",
                    'type': 'ticket'
                }
                
                tickets.append(ticket_data)
                count += 1
                
                # Add small delay to respect rate limits
                if count % 100 == 0:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Error fetching Zendesk tickets: {e}")
            raise
            
        logger.info(f"Fetched {len(tickets)} tickets from Zendesk")
        return tickets
    
    async def get_help_center_articles(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """
        Fetch help center articles from Zendesk
        
        Args:
            limit: Maximum number of articles to fetch
            
        Returns:
            List of article dictionaries
        """
        articles = []
        try:
            count = 0
            for article in self.client.help_center.articles():
                if count >= limit:
                    break
                    
                article_data = {
                    'id': article.id,
                    'title': article.title or '',
                    'body': article.body or '',
                    'section_id': article.section_id,
                    'author_id': article.author_id,
                    'created_at': article.created_at.isoformat() if article.created_at else None,
                    'updated_at': article.updated_at.isoformat() if article.updated_at else None,
                    'draft': article.draft,
                    'promoted': article.promoted,
                    'label_names': article.label_names or [],
                    'locale': article.locale,
                    'url': article.html_url,
                    'type': 'article'
                }
                
                articles.append(article_data)
                count += 1
                
                # Add small delay to respect rate limits
                if count % 100 == 0:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"Error fetching Zendesk articles: {e}")
            raise
            
        logger.info(f"Fetched {len(articles)} articles from Zendesk")
        return articles
    
    async def test_connection(self) -> bool:
        """
        Test the Zendesk connection
        
        Returns:
            True if connection is successful
        """
        try:
            # Try to fetch user info as a connection test
            user = self.client.users.me()
            return user is not None
        except Exception as e:
            logger.error(f"Zendesk connection test failed: {e}")
            return False

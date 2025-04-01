from pymongo import MongoClient
import yaml
from typing import Dict, List
from datetime import datetime

class MongoDBClient:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        db_config = self.config['database']
        self.client = MongoClient(db_config['mongodb_uri'])
        self.db = self.client[db_config['database_name']]
        self.collection = self.db[db_config['collection_name']]
    
    def insert_product(self, product_info: Dict) -> str:
        """
        Insert a product into the database.
        
        Args:
            product_info (Dict): Product information to insert
            
        Returns:
            str: ID of the inserted document
        """
        # Add timestamp
        product_info['processed_date'] = datetime.utcnow()
        
        # Insert document
        result = self.collection.insert_one(product_info)
        return str(result.inserted_id)
    
    def get_product(self, product_id: str) -> Dict:
        """
        Retrieve a product from the database.
        
        Args:
            product_id (str): ID of the product to retrieve
            
        Returns:
            Dict: Product information
        """
        return self.collection.find_one({'_id': product_id})
    
    def get_all_products(self) -> List[Dict]:
        """
        Retrieve all products from the database.
        
        Returns:
            List[Dict]: List of all products
        """
        return list(self.collection.find())
    
    def update_product(self, product_id: str, product_info: Dict) -> bool:
        """
        Update a product in the database.
        
        Args:
            product_id (str): ID of the product to update
            product_info (Dict): Updated product information
            
        Returns:
            bool: True if update was successful
        """
        result = self.collection.update_one(
            {'_id': product_id},
            {'$set': product_info}
        )
        return result.modified_count > 0
    
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product from the database.
        
        Args:
            product_id (str): ID of the product to delete
            
        Returns:
            bool: True if deletion was successful
        """
        result = self.collection.delete_one({'_id': product_id})
        return result.deleted_count > 0 
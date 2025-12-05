#!/usr/bin/env python3
"""
Document Upload and Processing System
Handles CSV, PDF, Excel, and other file types for data import and processing
Supports e-commerce data import, report processing, and document analysis
"""

import asyncio
import os
import uuid
import logging
import mimetypes
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from enum import Enum
import json
import pandas as pd
import PyPDF2
from io import BytesIO, StringIO
import csv
from dataclasses import dataclass
import httpx

# For document parsing
try:
    import openpyxl  # Excel files
except ImportError:
    openpyxl = None

try:
    import docx  # Word documents
except ImportError:
    docx = None

logger = logging.getLogger(__name__)

class DocumentType(str, Enum):
    """Supported document types"""
    CSV = "csv"
    PDF = "pdf" 
    EXCEL = "excel"
    JSON = "json"
    TXT = "txt"
    DOCX = "docx"
    TSV = "tsv"
    XML = "xml"

class ProcessingStatus(str, Enum):
    """Document processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    READY = "ready"

@dataclass
class DocumentMetadata:
    """Document metadata"""
    file_id: str
    filename: str
    file_type: DocumentType
    file_size: int
    upload_time: datetime
    tenant_id: str
    user_id: str
    status: ProcessingStatus
    processing_result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    preview_data: Optional[Dict[str, Any]] = None

@dataclass
class ProcessingOptions:
    """Document processing options"""
    extract_text: bool = True
    parse_tables: bool = True
    analyze_structure: bool = True
    extract_entities: bool = False
    generate_summary: bool = False
    import_to_ecommerce: bool = False
    create_workflow: bool = False
    
class DocumentProcessor:
    """Main document processing class"""
    
    def __init__(self, storage_path: str = "/tmp/bizosaas_documents"):
        self.storage_path = storage_path
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.supported_types = {
            'text/csv': DocumentType.CSV,
            'application/pdf': DocumentType.PDF,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': DocumentType.EXCEL,
            'application/vnd.ms-excel': DocumentType.EXCEL,
            'application/json': DocumentType.JSON,
            'text/plain': DocumentType.TXT,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': DocumentType.DOCX,
            'text/tab-separated-values': DocumentType.TSV,
            'application/xml': DocumentType.XML,
            'text/xml': DocumentType.XML
        }
        
        # Ensure storage directory exists
        os.makedirs(self.storage_path, exist_ok=True)
    
    async def upload_document(
        self, 
        file_data: bytes, 
        filename: str, 
        tenant_id: str, 
        user_id: str,
        content_type: Optional[str] = None
    ) -> DocumentMetadata:
        """Upload and validate document"""
        
        # Generate unique file ID
        file_id = f"doc_{uuid.uuid4().hex[:12]}"
        
        # Validate file size
        if len(file_data) > self.max_file_size:
            raise ValueError(f"File size {len(file_data)} exceeds maximum {self.max_file_size}")
        
        # Determine file type
        if not content_type:
            content_type, _ = mimetypes.guess_type(filename)
        
        if content_type not in self.supported_types:
            raise ValueError(f"Unsupported file type: {content_type}")
        
        file_type = self.supported_types[content_type]
        
        # Save file to storage
        file_path = os.path.join(self.storage_path, f"{file_id}_{filename}")
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Create metadata
        metadata = DocumentMetadata(
            file_id=file_id,
            filename=filename,
            file_type=file_type,
            file_size=len(file_data),
            upload_time=datetime.utcnow(),
            tenant_id=tenant_id,
            user_id=user_id,
            status=ProcessingStatus.UPLOADED
        )
        
        logger.info(f"Document uploaded: {filename} ({file_type}) for tenant {tenant_id}")
        return metadata
    
    async def process_document(
        self, 
        metadata: DocumentMetadata, 
        options: ProcessingOptions = ProcessingOptions()
    ) -> DocumentMetadata:
        """Process uploaded document based on type and options"""
        
        try:
            metadata.status = ProcessingStatus.PROCESSING
            file_path = os.path.join(self.storage_path, f"{metadata.file_id}_{metadata.filename}")
            
            # Process based on file type
            if metadata.file_type == DocumentType.CSV:
                result = await self.process_csv(file_path, options)
            elif metadata.file_type == DocumentType.PDF:
                result = await self.process_pdf(file_path, options)
            elif metadata.file_type == DocumentType.EXCEL:
                result = await self.process_excel(file_path, options)
            elif metadata.file_type == DocumentType.JSON:
                result = await self.process_json(file_path, options)
            elif metadata.file_type == DocumentType.TXT:
                result = await self.process_text(file_path, options)
            else:
                result = {"message": f"Processing for {metadata.file_type} not implemented yet"}
            
            metadata.processing_result = result
            metadata.status = ProcessingStatus.COMPLETED
            
            # Generate preview data
            metadata.preview_data = self.generate_preview(result, metadata.file_type)
            
            logger.info(f"Document processed successfully: {metadata.filename}")
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            metadata.status = ProcessingStatus.FAILED
            metadata.error_message = str(e)
        
        return metadata
    
    async def process_csv(self, file_path: str, options: ProcessingOptions) -> Dict[str, Any]:
        """Process CSV files - common for e-commerce data imports"""
        
        result = {
            "type": "csv_data",
            "rows": 0,
            "columns": [],
            "column_types": {},
            "sample_data": [],
            "summary": {},
            "ecommerce_detected": False,
            "import_ready": False
        }
        
        try:
            # Read CSV with pandas
            df = pd.read_csv(file_path)
            result["rows"] = len(df)
            result["columns"] = list(df.columns)
            
            # Analyze column types
            for col in df.columns:
                result["column_types"][col] = str(df[col].dtype)
            
            # Get sample data (first 5 rows)
            result["sample_data"] = df.head(5).to_dict('records')
            
            # Generate summary statistics
            result["summary"] = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "memory_usage": df.memory_usage().sum(),
                "null_counts": df.isnull().sum().to_dict()
            }
            
            # Detect e-commerce data patterns
            ecommerce_columns = [
                'product_id', 'sku', 'name', 'title', 'price', 'cost', 'category',
                'description', 'image', 'inventory', 'stock', 'weight', 'brand',
                'vendor', 'tags', 'variants', 'barcode', 'asin', 'upc'
            ]
            
            detected_ecommerce = []
            for col in df.columns:
                col_lower = col.lower()
                for ecom_col in ecommerce_columns:
                    if ecom_col in col_lower:
                        detected_ecommerce.append(col)
                        break
            
            if detected_ecommerce:
                result["ecommerce_detected"] = True
                result["ecommerce_columns"] = detected_ecommerce
                result["import_ready"] = len(detected_ecommerce) >= 3  # Need at least 3 key fields
                
                # Suggest mapping for e-commerce import
                result["suggested_mapping"] = self.suggest_ecommerce_mapping(df.columns)
            
            # If options specify e-commerce import, prepare import data
            if options.import_to_ecommerce and result["ecommerce_detected"]:
                result["import_data"] = await self.prepare_ecommerce_import(df, result["suggested_mapping"])
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"CSV processing error: {e}")
        
        return result
    
    async def process_pdf(self, file_path: str, options: ProcessingOptions) -> Dict[str, Any]:
        """Process PDF files - extract text and analyze structure"""
        
        result = {
            "type": "pdf_document",
            "pages": 0,
            "text_content": "",
            "summary": {},
            "tables_detected": False,
            "entities": []
        }
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                result["pages"] = len(pdf_reader.pages)
                
                # Extract text from all pages
                text_content = []
                for page in pdf_reader.pages:
                    text_content.append(page.extract_text())
                
                result["text_content"] = "\n".join(text_content)
                result["word_count"] = len(result["text_content"].split())
                
                # Generate summary
                result["summary"] = {
                    "page_count": result["pages"],
                    "word_count": result["word_count"],
                    "character_count": len(result["text_content"]),
                    "estimated_reading_time": f"{result['word_count'] // 200} minutes"
                }
                
                # Detect if this might be a report or data document
                if any(keyword in result["text_content"].lower() for keyword in 
                      ['table', 'data', 'report', 'analysis', 'revenue', 'sales']):
                    result["tables_detected"] = True
                    result["document_category"] = "report"
                else:
                    result["document_category"] = "general"
                
                # Extract first 500 characters as preview
                result["preview_text"] = result["text_content"][:500] + "..." if len(result["text_content"]) > 500 else result["text_content"]
                
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"PDF processing error: {e}")
        
        return result
    
    async def process_excel(self, file_path: str, options: ProcessingOptions) -> Dict[str, Any]:
        """Process Excel files - similar to CSV but with multi-sheet support"""
        
        result = {
            "type": "excel_workbook",
            "sheets": [],
            "total_rows": 0,
            "ecommerce_detected": False,
            "import_ready": False
        }
        
        try:
            if openpyxl is None:
                raise ImportError("openpyxl not installed - cannot process Excel files")
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                sheet_data = {
                    "name": sheet_name,
                    "rows": len(df),
                    "columns": list(df.columns),
                    "column_types": {col: str(df[col].dtype) for col in df.columns},
                    "sample_data": df.head(3).to_dict('records')
                }
                
                # Check for e-commerce data in this sheet
                ecommerce_columns = [
                    'product', 'sku', 'price', 'inventory', 'category', 'name', 'title'
                ]
                ecom_found = any(any(ecom in col.lower() for ecom in ecommerce_columns) 
                               for col in df.columns)
                
                if ecom_found:
                    sheet_data["ecommerce_detected"] = True
                    result["ecommerce_detected"] = True
                    sheet_data["suggested_mapping"] = self.suggest_ecommerce_mapping(df.columns)
                
                result["sheets"].append(sheet_data)
                result["total_rows"] += len(df)
            
            result["import_ready"] = result["ecommerce_detected"]
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Excel processing error: {e}")
        
        return result
    
    async def process_json(self, file_path: str, options: ProcessingOptions) -> Dict[str, Any]:
        """Process JSON files - API responses, configuration data"""
        
        result = {
            "type": "json_data",
            "structure": {},
            "keys": [],
            "array_detected": False,
            "import_ready": False
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            result["structure"] = self.analyze_json_structure(data)
            
            if isinstance(data, list):
                result["array_detected"] = True
                result["item_count"] = len(data)
                if len(data) > 0:
                    result["sample_item"] = data[0]
                    result["keys"] = list(data[0].keys()) if isinstance(data[0], dict) else []
            elif isinstance(data, dict):
                result["keys"] = list(data.keys())
                result["sample_data"] = {k: v for k, v in list(data.items())[:5]}
            
            # Check if this could be product/e-commerce data
            ecommerce_keys = ['products', 'items', 'sku', 'price', 'name', 'category']
            if any(key in str(result["keys"]).lower() for key in ecommerce_keys):
                result["ecommerce_detected"] = True
                result["import_ready"] = True
                
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"JSON processing error: {e}")
        
        return result
    
    async def process_text(self, file_path: str, options: ProcessingOptions) -> Dict[str, Any]:
        """Process plain text files"""
        
        result = {
            "type": "text_document",
            "content": "",
            "word_count": 0,
            "line_count": 0,
            "summary": {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            result["content"] = content
            result["word_count"] = len(content.split())
            result["line_count"] = len(content.split('\n'))
            result["character_count"] = len(content)
            
            result["summary"] = {
                "word_count": result["word_count"],
                "line_count": result["line_count"], 
                "character_count": result["character_count"],
                "estimated_reading_time": f"{result['word_count'] // 200} minutes"
            }
            
            # Preview first 300 characters
            result["preview"] = content[:300] + "..." if len(content) > 300 else content
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Text processing error: {e}")
        
        return result
    
    def suggest_ecommerce_mapping(self, columns: List[str]) -> Dict[str, str]:
        """Suggest mapping between CSV columns and e-commerce fields"""
        
        mapping_patterns = {
            'product_id': ['id', 'product_id', 'sku', 'item_id', 'product_sku'],
            'name': ['name', 'title', 'product_name', 'item_name', 'product_title'],
            'description': ['description', 'desc', 'product_description', 'details'],
            'price': ['price', 'cost', 'amount', 'price_usd', 'retail_price'],
            'category': ['category', 'cat', 'product_category', 'type', 'section'],
            'brand': ['brand', 'manufacturer', 'make', 'vendor', 'supplier'],
            'inventory': ['inventory', 'stock', 'quantity', 'qty', 'stock_level'],
            'weight': ['weight', 'wt', 'mass', 'shipping_weight'],
            'image': ['image', 'photo', 'picture', 'image_url', 'thumbnail'],
            'barcode': ['barcode', 'upc', 'ean', 'gtin', 'asin']
        }
        
        suggested_mapping = {}
        columns_lower = [col.lower() for col in columns]
        
        for ecom_field, patterns in mapping_patterns.items():
            for col, col_lower in zip(columns, columns_lower):
                if any(pattern in col_lower for pattern in patterns):
                    suggested_mapping[ecom_field] = col
                    break
        
        return suggested_mapping
    
    async def prepare_ecommerce_import(self, df: pd.DataFrame, mapping: Dict[str, str]) -> Dict[str, Any]:
        """Prepare data for e-commerce platform import"""
        
        import_data = {
            "products": [],
            "total_products": len(df),
            "valid_products": 0,
            "validation_errors": []
        }
        
        required_fields = ['product_id', 'name', 'price']
        missing_required = [field for field in required_fields if field not in mapping]
        
        if missing_required:
            import_data["validation_errors"].append(f"Missing required fields: {missing_required}")
            return import_data
        
        for idx, row in df.iterrows():
            try:
                product = {}
                
                # Map fields according to suggested mapping
                for ecom_field, csv_column in mapping.items():
                    if csv_column in df.columns:
                        value = row[csv_column]
                        if pd.notna(value):  # Only include non-null values
                            product[ecom_field] = value
                
                # Validate required fields
                if all(field in product for field in ['product_id', 'name']):
                    import_data["products"].append(product)
                    import_data["valid_products"] += 1
                else:
                    import_data["validation_errors"].append(f"Row {idx}: Missing required data")
                    
            except Exception as e:
                import_data["validation_errors"].append(f"Row {idx}: {str(e)}")
        
        return import_data
    
    def analyze_json_structure(self, data: Any, depth: int = 0, max_depth: int = 3) -> Dict[str, Any]:
        """Analyze JSON structure recursively"""
        
        if depth > max_depth:
            return {"truncated": True}
        
        if isinstance(data, dict):
            return {
                "type": "object",
                "keys": list(data.keys()),
                "properties": {k: self.analyze_json_structure(v, depth + 1, max_depth) 
                              for k, v in list(data.items())[:5]}  # Limit to first 5 properties
            }
        elif isinstance(data, list):
            return {
                "type": "array",
                "length": len(data),
                "items": self.analyze_json_structure(data[0], depth + 1, max_depth) if data else None
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:50] + "..." if len(str(data)) > 50 else str(data)
            }
    
    def generate_preview(self, processing_result: Dict[str, Any], file_type: DocumentType) -> Dict[str, Any]:
        """Generate preview data for frontend display"""
        
        preview = {
            "type": file_type,
            "processed": True,
            "summary": {}
        }
        
        if file_type == DocumentType.CSV:
            preview.update({
                "columns": processing_result.get("columns", []),
                "sample_rows": processing_result.get("sample_data", [])[:3],
                "row_count": processing_result.get("rows", 0),
                "ecommerce_ready": processing_result.get("import_ready", False)
            })
            
        elif file_type == DocumentType.PDF:
            preview.update({
                "pages": processing_result.get("pages", 0),
                "preview_text": processing_result.get("preview_text", ""),
                "document_type": processing_result.get("document_category", "general")
            })
            
        elif file_type == DocumentType.EXCEL:
            preview.update({
                "sheets": [sheet["name"] for sheet in processing_result.get("sheets", [])],
                "total_rows": processing_result.get("total_rows", 0),
                "ecommerce_ready": processing_result.get("import_ready", False)
            })
        
        return preview
    
    def cleanup_file(self, file_id: str, filename: str) -> bool:
        """Clean up uploaded file"""
        try:
            file_path = os.path.join(self.storage_path, f"{file_id}_{filename}")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            logger.error(f"File cleanup error: {e}")
        return False

# Global document processor instance
document_processor = DocumentProcessor()

async def get_document_processor() -> DocumentProcessor:
    """Get document processor instance"""
    return document_processor
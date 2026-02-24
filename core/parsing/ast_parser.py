import ast
import os
from typing import List
import logging


from utils.logging.logger import setup_logging

logger = logging.getLogger(__name__)

class ASTParser:
    """
    Parses Python files using AST and extracts structured code chunks.
    """

    def parse_file(self, file_path:str) -> List[CodeChunk]:
        """
        Parse a single Python file and return extracted code chunks
        """
        chunks = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return chunks
        
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            logger.warning(f"Syntax error in file {file_path}: {e}")
            return chunks
        
        source_lines = source_code.splitlines()

        for node in ast.walk(tree):
            #collecting function definitions
            if isinstance(node, ast.FunctionDef): #FunctionDef filters functions from the source code 
                chunk = self._create_chunk(
                    node=node,
                    file_path=file_path,
                    source_lines=source_lines,
                    chunk_type='function'
                )
                chunks.append(chunk)

            #Collecting class definitions
            elif isinstance(node, ast.ClassDef): #ClassDef filters classes from the source code
                class_chunk = self._create_chunk(
                    node=node,
                    file_path=file_path,
                    source_lines=source_lines,
                    chunk_type='class'
                )
                chunks.append(class_chunk)

                #Method extraction
                for body_item in node.body:
                    if isinstance(body_item, ast.FunctionDef):
                        method_chunk = self._create_chunk(
                            node=body_item,
                            file_path=file_path,
                            source_lines=source_lines,
                            chunk_type="method"
                        )
                        chunks.append(method_chunk)
        
        logger.info(f"Parsed {len(chunks)} chunks from {file_path}")
        return chunks
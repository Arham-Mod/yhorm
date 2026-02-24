import ast
import os
from typing import List
import logging


from core.parsing.chunk_model import CodeChunk

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
    
    def parse_repository(self, file_paths:str) -> List[CodeChunk]:
        """
        Parsing all python files in the repo
        """
        
        all_chunks=[]

        for file_path in file_paths:
            file_chunks = self.parse_file(file_path)
            all_chunks.extend(file_chunks)


        logger.info(f"Total chunks parsed from repository: {len(all_chunks)}")
        return all_chunks


    def _create_chunk(self, node, file_path: str, source_lines: List[str], chunk_type: str) -> CodeChunk:
        """
        Create a CodeChunk object from AST node.
        """

        start_line = node.lineno
        end_line = getattr(node, "end_lineno", start_line)

        # Extract source code block
        source_code = "\n".join(source_lines[start_line - 1:end_line])

        # Extract called functions
        calls = self._extract_calls(node)

        chunk_id = f"{os.path.basename(file_path)}:{node.name}:{start_line}"

        return CodeChunk(
            id=chunk_id,
            file_path=file_path,
            name=node.name,
            type=chunk_type,
            start_line=start_line,
            end_line=end_line,
            source_code=source_code,
            calls=calls
        )
    
    def _extract_calls(self, node) -> List[str]:
        """
        Extract simple function calls inside a node.
        """
        calls = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):

                # Simple function call: foo()
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)

                # Method call: obj.method()
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

        return list(set(calls))  # remove duplicates

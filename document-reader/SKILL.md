---
name: document-reader
description: Use when reading document files to extract API endpoints, schemas, backend logic, or production code patterns for integration and implementation tasks
---

# Document Reader

## Overview
Read document files with line-based size strategy. Files with ≤500 lines: read entirely. Files with >500 lines: read in chunks ensuring complete coverage. Specialized extraction for API integrations, schemas, and production code.

## When to Use
- Reading API documentation to extract endpoints, request/response formats
- Extracting JSON schemas, TypeScript interfaces, or database schemas from docs
- Finding backend logic patterns (services, controllers, business rules)
- Retrieving production-ready code examples for integration
- Converting documentation to typed interfaces or SDKs

## Core Pattern
```python
# Count lines to determine size
def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return sum(1 for _ in f)

# Choose reading strategy
def read_file(file_path):
    line_count = count_lines(file_path)
    return open(file_path).read() if line_count <= 500 else read_in_chunks(file_path)

# Extract sections by pattern
def extract_pattern(content, pattern):
    import re
    return re.findall(pattern, content, re.MULTILINE)
```

### Guaranteed Full Coverage Reading

This module ensures every single line of the document is read and verified - critical for API docs where missing a constraint can cause integration bugs.

```python
class CoverageError(Exception):
    """Raised when full file coverage cannot be verified."""
    pass

def read_document_guaranteed(file_path, verify_coverage=True):
    """
    Read entire file with guaranteed coverage verification.
    
    Args:
        file_path: Path to document
        verify_coverage: If True, verify all lines were read
    
    Returns:
        dict with 'content' and 'coverage_info'
    
    Raises:
        CoverageError: If coverage verification fails
    """
    line_count = count_lines(file_path)
    
    if line_count <= 500:
        content = read_text_file(file_path)
        coverage = {
            'strategy': 'full',
            'lines_read': line_count,
            'lines_total': line_count,
            'verified': True if verify_coverage else None
        }
    else:
        chunks = []
        lines_read = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            while True:
                chunk = []
                for _ in range(500):
                    line = f.readline()
                    if not line:
                        break
                    chunk.append(line)
                    lines_read += 1
                
                if not chunk:
                    break
                chunks.append(''.join(chunk))
        
        content = '\n'.join(chunks)
        coverage = {
            'strategy': 'chunked',
            'chunks': len(chunks),
            'lines_read': lines_read,
            'lines_total': line_count,
            'verified': lines_read == line_count if verify_coverage else None
        }
    
    if verify_coverage and coverage['lines_read'] != coverage['lines_total']:
        raise CoverageError(
            f"Coverage gap: read {coverage['lines_read']} of {coverage['lines_total']} lines"
        )
    
    return {'content': content, 'coverage': coverage}
```

**When to use:** API specs, schemas, contracts where missing content causes bugs.

### Structured Context Index

This module organizes all extracted data into a single source of truth - preventing fragmented understanding.

```python
class ContextIndex:
    """
    Structured index that organizes all extracted data into a single source of truth.
    Prevents fragmented understanding by maintaining unified data structure.
    """
    
    def __init__(self):
        self.endpoints = []
        self.schemas = {}
        self.services = []
        self.controllers = []
        self.models = []
        self.auth = {}
        self.errors = []
        self.metadata = {
            'files_processed': [],
            'extraction_timestamp': None,
            'coverage_verified': False
        }
    
    def add_endpoint(self, method, path, description=None, request_schema=None, response_schema=None):
        self.endpoints.append({
            'method': method.upper(),
            'path': path,
            'description': description,
            'request': request_schema,
            'response': response_schema
        })
    
    def add_schema(self, name, schema_type, definition):
        self.schemas[name] = {
            'type': schema_type,
            'definition': definition,
            'used_by': []
        }
    
    def link_schema_to_endpoint(self, schema_name, endpoint_path):
        if schema_name in self.schemas:
            self.schemas[schema_name]['used_by'].append(endpoint_path)
    
    def add_service(self, name, methods):
        self.services.append({'name': name, 'methods': methods})
    
    def add_controller(self, name, routes):
        self.controllers.append({'name': name, 'routes': routes})
    
    def add_model(self, name, fields):
        self.models.append({'name': name, 'fields': fields})
    
    def add_auth(self, auth_type, details):
        self.auth[auth_type] = details
    
    def add_error(self, error_type, handling):
        self.errors.append({'type': error_type, 'handling': handling})
    
    def to_dict(self):
        return {
            'endpoints': self.endpoints,
            'schemas': self.schemas,
            'services': self.services,
            'controllers': self.controllers,
            'models': self.models,
            'auth': self.auth,
            'errors': self.errors,
            'metadata': self.metadata
        }
    
    def validate(self):
        """Validate index consistency."""
        issues = []
        
        for endpoint in self.endpoints:
            if endpoint.get('request'):
                if not any(endpoint['request'] in s for s in self.schemas.keys()):
                    issues.append(f"Endpoint {endpoint['path']} references unknown request schema")
        
        return issues
```

**Use:** build_context_index(file_paths) to create unified index from multiple files.

### API Integration Extraction
```python
def extract_api_endpoints(content):
    patterns = [
        r'(GET|POST|PUT|PATCH|DELETE)\s+([^\s]+)',  # REST endpoints
        r'@(?:Get|Post|Put|Patch|Delete)\([^\)]+\)',  # decorators
        r'endpoint[:\s]+([^\n]+)',  # OpenAPI style
    ]
    endpoints = []
    for p in patterns:
        endpoints.extend(re.findall(p, content, re.IGNORECASE))
    return endpoints

def extract_request_response(content):
    import re
    requests = re.findall(r'(?:request|Request)[\s\S]{0,200}(?:\{[\s\S]*?\})', content)
    responses = re.findall(r'(?:response|Response)[\s\S]{0,200}(?:\{[\s\S]*?\})', content)
    return {'requests': requests, 'responses': responses}

def extract_auth_info(content):
    import re
    patterns = {
        'bearer': r'(?:Bearer|token)[:\s]+([^\s\n]+)',
        'api_key': r'(?:api[_-]?key|API[_-]?KEY)[:\s]+([^\s\n]+)',
        'basic': r'(?:basic\s+auth|Basic\s+Auth)',
        'oauth': r'(?:oauth|OAuth|oauth2|OAuth2)',
    }
    found = {}
    for auth_type, pattern in patterns.items():
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            found[auth_type] = matches
    return found
```

### Schema Extraction
```python
def extract_json_schemas(content):
    import re
    schemas = re.findall(r'\{[\s\S]*?"type"\s*:\s*"object"[\s\S]*?\}', content)
    return [json.loads(s) for s in schemas if valid_json(s)]

def extract_typescript_interfaces(content):
    import re
    interfaces = re.findall(r'interface\s+(\w+)\s*\{([^}]+)\}', content)
    return {name: props for name, props in interfaces}

def extract_database_schemas(content):
    import re
    tables = re.findall(r'CREATE\s+TABLE\s+(\w+)', content, re.IGNORECASE)
    columns = re.findall(r'(\w+)\s+(?:INT|VARCHAR|TEXT|BOOLEAN|DATE|TIMESTAMP)', content, re.IGNORECASE)
    return {'tables': tables, 'columns': columns}

def extract_openapi_spec(content):
    import re
    paths = re.findall(r'/[^/\s]+', content)
    methods = re.findall(r'(get|post|put|patch|delete):\s*', content, re.IGNORECASE)
    return {'paths': list(set(paths)), 'methods': list(set(methods))}
```

### Backend Logic Extraction
```python
def extract_services(content):
    import re
    services = re.findall(r'class\s+(\w*Service\w*).*?:', content)
    methods = re.findall(r'def\s+(\w+)\s*\([\s\S]*?\):', content)
    return {'services': services, 'methods': methods}

def extract_controllers(content):
    import re
    controllers = re.findall(r'class\s+(\w*Controller\w*).*?:', content)
    routes = re.findall(r'@(?:Get|Post|Put|Delete)\s*\([^\)]+\)', content)
    return {'controllers': controllers, 'routes': routes}

def extract_models(content):
    import re
    models = re.findall(r'class\s+(\w*Model\w*).*?:', content)
    fields = re.findall(r'(\w+)\s*=\s*(?:Field|Column|Property)', content)
    return {'models': models, 'fields': fields}

def extract_validators(content):
    import re
    validators = re.findall(r'@validator|@validates|class\s+(\w*Validator\w*)', content)
    rules = re.findall(r'(?:@min|@max|@required|@pattern)\s*\([^\)]+\)', content)
    return {'validators': validators, 'rules': rules}
```

### Production Code Patterns
```python
def extract_error_handling(content):
    import re
    try_catch = re.findall(r'try\s*\{[^}]+\}[^}]*catch\s*\([^)]+\)\s*\{[^}]+\}', content)
    error_types = re.findall(r'except\s+(\w+Error)', content)
    return {'try_catch': try_catch, 'error_types': error_types}

def extract_logging(content):
    import re
    logs = re.findall(r'(?:logger|logging|log)\.(?:info|error|debug|warning)\s*\([^)]+\)', content)
    return logs

def extract_typed_interfaces(content):
    import re
    interfaces = re.findall(r'(?:interface|Type|type)\s+(\w+)\s*[:{]', content)
    return interfaces
```

## Quick Reference

| Format | Library | Primary Use |
|--------|---------|-------------|
| .txt, .md | built-in open() | Full reading, regex search |
| .pdf | PyPDF2 | Text extraction from PDFs |
| .docx | python-docx | Paragraph/text extraction |

### Extraction Quick Reference

| Data Type | Function | Pattern/Method |
|-----------|----------|----------------|
| API endpoints | `extract_api_endpoints()` | GET/POST/PUT/DELETE patterns |
| Request/Response | `extract_request_response()` | JSON in context |
| Auth info | `extract_auth_info()` | Bearer, API key, OAuth |
| JSON schemas | `extract_json_schemas()` | type: "object" |
| TypeScript interfaces | `extract_typescript_interfaces()` | interface declarations |
| Database schemas | `extract_database_schemas()` | CREATE TABLE, column types |
| Services | `extract_services()` | *Service class patterns |
| Controllers | `extract_controllers()` | @Get, @Post decorators |
| Models | `extract_models()` | *Model class patterns |
| Error handling | `extract_error_handling()` | try/catch, except blocks |
| Logging | `extract_logging()` | logger.* patterns |
| Validators | `extract_validators()` | @validator, @validates |

## Implementation

### Text Files (TXT, MD)
```python
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def search_in_text(file_path, pattern):
    content = read_text_file(file_path)
    import re
    return re.findall(pattern, content, re.MULTILINE)

def extract_functions(content):
    import re
    return re.findall(r'^def\s+\w+.*$', content, re.MULTILINE)

def extract_code_blocks(content):
    import re
    return re.findall(r'```[\s\S]*?```', content)
```

### PDF Files
```python
import PyPDF2

def read_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_from_pdf(file_path, pattern):
    content = read_pdf(file_path)
    import re
    return re.findall(pattern, content)
```

### DOCX Files
```python
import docx

def read_docx(file_path):
    doc = docx.Document(file_path)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return '\n'.join(paragraphs)

def extract_tables(docx_path):
    doc = docx.Document(docx_path)
    tables = []
    for table in doc.tables:
        rows = [[cell.text for cell in row.cells] for row in table.rows]
        tables.append(rows)
    return tables
```

### Big File Chunk Reading (Critical for >500 lines)
```python
def read_in_chunks(file_path, chunk_lines=500):
    all_content = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        while True:
            chunk = []
            for _ in range(chunk_lines):
                line = f.readline()
                if not line:
                    break
                chunk.append(line)
            if not chunk:
                break
            all_content.append(''.join(chunk))
    return '\n'.join(all_content)

def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return sum(1 for _ in f)
```

### Complete File Reading with Size Detection
```python
def read_document(file_path):
    line_count = count_lines(file_path)
    
    if line_count <= 500:
        return read_text_file(file_path)
    else:
        return read_in_chunks(file_path, chunk_lines=500)

def read_and_search(file_path, pattern):
    content = read_document(file_path)
    import re
    return re.findall(pattern, content, re.MULTILINE)
```

## Common Mistakes

1. **Not counting lines first** - Jump directly to reading without checking file size
2. **Forgetting complete coverage** - Read partial content from large files and miss content at the end
3. **Ignoring encoding** - Not handling encoding errors with `errors='ignore'`
4. **PDF text extraction limitations** - Scanned PDFs (images) require OCR; won't extract from images
5. **DOCX tables** - Default extraction only gets paragraphs, not tables (need explicit table handling)
6. **Binary files** - Trying to read PDFs/DOCXs as text (use 'rb' mode for PDFs, use libraries for DOCX)
7. **No chunk iteration** - For big files, just reading once misses content beyond first chunk
8. **API extraction too broad** - Don't just grep "endpoint"; look for full request/response pairs
9. **Missing authentication** - Always extract auth patterns (Bearer, API key, OAuth) for integration
10. **Schema without validation** - Extract JSON schema but forget to validate extracted JSON is valid
11. **Ignoring error patterns** - Production code needs error handling; extract try/catch and error types
12. **No type safety** - Extract TypeScript interfaces alongside code for typed SDK generation
13. **Skipping coverage verification** - For critical docs (API specs, contracts), always verify complete read
14. **Ignoring CoverageError** - If coverage verification fails, don't ignore it and proceed anyway
15. **No unified index** - Extracting data without organizing into single source of truth
16. **Inconsistent field names** - Using userId in one place, user_id in another (causes runtime bugs)
17. **Duplicate schemas** - Defining same schema multiple times instead of reusing
18. **No consistency validation** - Not running FieldNameValidator or SchemaReuseValidator
19. **Silent assumptions** - Making assumptions without documenting what was assumed
20. **No confidence tracking** - Treating extracted data with equal confidence regardless of source quality

## Red Flags - STOP

- Reading file without checking line count
- Assuming 1000+ line files can be read all at once
- Not ensuring complete file coverage for large files
- Using Read tool on binary formats (PDF, DOCX) without conversion
- Reading critical API docs without guaranteed coverage verification
- Using extracted data without checking assumption report

## Consistency Enforcement

This module prevents subtle bugs from inconsistent field names and duplicate schemas - very common in API work.

```python
import json
import re

class FieldNameValidator:
    """
    Enforces consistent field names across extracted data.
    Prevents subtle bugs from inconsistent naming (e.g., userId vs user_id vs user-id).
    """
    
    STANDARD_FIELDS = {
        'id': ['id', 'ID', 'Id', '_id', 'id_'],
        'created_at': ['created_at', 'createdAt', 'created', 'createdOn', 'timestamp'],
        'updated_at': ['updated_at', 'updatedAt', 'modified', 'modifiedAt'],
        'deleted_at': ['deleted_at', 'deletedAt', 'deleted', 'removedAt', 'is_deleted'],
        'user_id': ['user_id', 'userId', 'user_id', 'userId', 'userID', 'user-id'],
        'api_key': ['api_key', 'apiKey', 'API_KEY', 'api-key', 'apikey'],
    }
    
    @classmethod
    def normalize(cls, field_name, target_standard='snake_case'):
        """Normalize field name to standard format."""
        if target_standard == 'snake_case':
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', field_name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        return field_name.lower()
    
    @classmethod
    def validate_consistency(cls, data_dict):
        """Check for inconsistent field naming in extracted data."""
        issues = []
        
        for standard, variants in cls.STANDARD_FIELDS.items():
            found_variants = set()
            for key in data_dict.keys():
                if any(v in key.lower() for v in variants):
                    found_variants.add(key)
            
            if len(found_variants) > 1:
                issues.append(f"Inconsistent naming for '{standard}': {found_variants}")
        
        return issues


class SchemaReuseValidator:
    """
    Ensures extracted schemas are reused consistently.
    Prevents duplicate definitions that cause subtle bugs.
    """
    
    @classmethod
    def find_duplicates(cls, schemas):
        """Find schemas with identical structure but different names."""
        normalized = {}
        
        for name, schema in schemas.items():
            normalized_def = json.dumps(schema.get('definition', {}), sort_keys=True)
            
            if normalized_def in normalized:
                normalized[normalized_def].append(name)
            else:
                normalized[normalized_def] = [name]
        
        return {k: v for k, v in normalized.items() if len(v) > 1}
    
    @classmethod
    def validate_reuse(cls, index):
        """Validate schemas are properly reused across endpoints."""
        issues = []
        
        duplicates = cls.find_duplicates(index.schemas)
        for _, names in duplicates.items():
            if len(names) > 1:
                issues.append(f"Duplicate schemas: {names}")
        
        for schema_name, schema in index.schemas.items():
            if not schema.get('used_by'):
                issues.append(f"Unused schema: {schema_name}")
        
        return issues


def validate_extraction(index):
    """
    Validate consistency of extracted data.
    
    Returns:
        dict with 'field_issues', 'schema_issues', 'is_valid'
    """
    field_issues = FieldNameValidator.validate_consistency(index.to_dict())
    schema_issues = SchemaReuseValidator.validate_reuse(index)
    
    return {
        'field_issues': field_issues,
        'schema_issues': schema_issues,
        'is_valid': len(field_issues) == 0 and len(schema_issues) == 0,
        'issues_count': len(field_issues) + len(schema_issues)
    }
```

**Example usage:**

```python
index = build_context_index(['api-docs.md'])
validation = validate_extraction(index)

if not validation['is_valid']:
    print(f"Validation issues: {validation['issues_count']}")
    for issue in validation['field_issues']:
        print(f"  Field issue: {issue}")
    for issue in validation['schema_issues']:
        print(f"  Schema issue: {issue}")
    raise ValidationError("Inconsistent data extracted")
```

## Assumption Tracking

This module explicitly tracks missing information and assumptions - preventing silent wrong logic from undocumented assumptions.

```python
from datetime import datetime

class AssumptionTracker:
    """
    Explicitly tracks missing information and assumptions made during extraction.
    Prevents silent wrong logic from undocumented assumptions.
    """
    
    def __init__(self):
        self.missing = []  # Explicitly missing data
        self.assumptions = []  # What we assumed to fill gaps
        self.confidence = []  # Confidence scores for extracted data
    
    def add_missing(self, field, expected_from, reason):
        """Record explicitly missing information."""
        self.missing.append({
            'field': field,
            'expected_from': expected_from,
            'reason': reason,
            'timestamp': str(datetime.now())
        })
    
    def add_assumption(self, field, assumption, evidence, confidence='medium'):
        """Record assumption made to fill a gap."""
        self.assumptions.append({
            'field': field,
            'assumption': assumption,
            'evidence': evidence,
            'confidence': confidence,
            'timestamp': str(datetime.now())
        })
    
    def add_confidence(self, field, score, reason):
        """Record confidence score for extracted data."""
        self.confidence.append({
            'field': field,
            'score': score,
            'reason': reason
        })
    
    def get_assumptions_report(self):
        """Generate human-readable assumptions report."""
        return {
            'missing_fields': self.missing,
            'assumptions_made': self.assumptions,
            'confidence_notes': self.confidence,
            'summary': f"Missing: {len(self.missing)}, Assumptions: {len(self.assumptions)}"
        }
    
    def has_low_confidence(self):
        """Check if any assumptions have low confidence."""
        return any(a['confidence'] == 'low' for a in self.assumptions)


def auto_detect_assumptions(content, index):
    """
    Automatically detect missing data and create assumptions.
    
    Args:
        content: Full document content
        index: ContextIndex with extracted data
    
    Returns:
        AssumptionTracker with detected gaps
    """
    tracker = AssumptionTracker()
    
    for endpoint in index.endpoints:
        if not endpoint.get('description'):
            tracker.add_missing(
                f"description for {endpoint['path']}",
                "endpoint documentation",
                "No description found"
            )
            tracker.add_assumption(
                f"description for {endpoint['path']}",
                "derived from HTTP method and path",
                f"{endpoint['method']} {endpoint['path']}",
                confidence='low'
            )
        
        if not endpoint.get('response'):
            tracker.add_missing(
                f"response schema for {endpoint['path']}",
                "API docs",
                "No response schema documented"
            )
    
    for schema_name, schema in index.schemas.items():
        if not schema.get('used_by'):
            tracker.add_assumption(
                f"schema {schema_name}",
                "may be unused or undocumented endpoint",
                "No endpoint references this schema",
                confidence='low'
            )
    
    return tracker


def extract_with_assumptions(file_path):
    """
    Complete extraction workflow with assumption tracking.
    
    Returns:
        dict with 'index', 'assumptions', 'validation'
    """
    result = read_document_guaranteed(file_path, verify_coverage=True)
    index = build_context_index([file_path])
    tracker = auto_detect_assumptions(result['content'], index)
    validation = validate_extraction(index)
    
    return {
        'content': result['content'],
        'index': index,
        'assumptions': tracker.get_assumptions_report(),
        'validation': validation,
        'warnings': tracker.has_low_confidence()
    }
```

## Edge Cases
- Exactly 500 lines: read entirely; 501+ uses chunked reading.

## Examples

**Example 1:** Extract API with ContextIndex + validation
```python
index = build_context_index(['api-docs.md'])
validation = validate_extraction(index)
if not validation['is_valid']:
    raise ValidationError(f"Issues: {validation['issues_count']}")
```

**Example 2:** Extract with assumption tracking
```python
result = extract_with_assumptions('api-docs.md')
if result['warnings']:
    print("STOP: Review assumptions before proceeding")
```
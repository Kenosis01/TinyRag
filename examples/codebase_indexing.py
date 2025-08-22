"""
Codebase indexing example for TinyRag
"""

from tinyrag import TinyRag
import tempfile
import os

def create_sample_code_files():
    """Create sample code files for demonstration"""
    temp_dir = tempfile.mkdtemp()
    
    # Python file
    python_code = '''
def authenticate_user(username, password):
    """Authenticate user with username and password"""
    if not username or not password:
        return False
    
    # Check against database
    user = get_user_from_db(username)
    return verify_password(user, password)

class UserManager:
    """Manages user operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_user(self, username, email):
        """Create a new user account"""
        user_data = {
            'username': username,
            'email': email,
            'created_at': datetime.now()
        }
        return self.db.insert('users', user_data)
'''
    
    # JavaScript file
    js_code = '''
function calculateTotal(items) {
    // Calculate total price of items
    return items.reduce((total, item) => {
        return total + (item.price * item.quantity);
    }, 0);
}

const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

class ShoppingCart {
    constructor() {
        this.items = [];
        this.total = 0;
    }
    
    addItem(item) {
        this.items.push(item);
        this.updateTotal();
    }
}
'''
    
    # Java file
    java_code = '''
public class DatabaseManager {
    private Connection connection;
    
    public DatabaseManager(String url) {
        this.connection = DriverManager.getConnection(url);
    }
    
    public List<User> getAllUsers() {
        String query = "SELECT * FROM users";
        PreparedStatement stmt = connection.prepareStatement(query);
        ResultSet rs = stmt.executeQuery();
        
        List<User> users = new ArrayList<>();
        while (rs.next()) {
            users.add(new User(rs.getString("username"), rs.getString("email")));
        }
        return users;
    }
}
'''
    
    # Write files
    with open(os.path.join(temp_dir, "auth.py"), "w") as f:
        f.write(python_code)
    
    with open(os.path.join(temp_dir, "cart.js"), "w") as f:
        f.write(js_code)
    
    with open(os.path.join(temp_dir, "DatabaseManager.java"), "w") as f:
        f.write(java_code)
    
    return temp_dir

def main():
    print("=== TinyRag Codebase Indexing Example ===\n")
    
    # Create sample code files
    code_dir = create_sample_code_files()
    print(f"Created sample code files in: {code_dir}")
    
    # Initialize TinyRag
    rag = TinyRag(vector_store="memory", max_workers=2)
    
    # Index the codebase
    print("\n=== Indexing Codebase ===")
    rag.add_codebase(code_dir, recursive=True)
    
    print(f"\nTotal indexed functions: {rag.get_chunk_count()}")
    
    # Example 1: Search for authentication functions
    print("\n=== Search for Authentication Functions ===")
    auth_results = rag.search_code("authentication login user", k=3)
    
    for i, (code, score) in enumerate(auth_results, 1):
        print(f"\n{i}. Score: {score:.3f}")
        lines = code.split('\n')
        print(f"   File: {lines[0].replace('File: ', '')}")
        print(f"   Function: {lines[3].replace('Name: ', '')}")
        print(f"   Language: {lines[1].replace('Language: ', '')}")
        print(f"   Code preview: {lines[5][:60]}...")
    
    # Example 2: Search by programming language
    print("\n=== Search Python Functions ===")
    python_results = rag.search_code("user management", k=2, language="python")
    
    for i, (code, score) in enumerate(python_results, 1):
        print(f"\n{i}. Score: {score:.3f}")
        lines = code.split('\n')
        print(f"   Function: {lines[3].replace('Name: ', '')}")
        print(f"   Type: {lines[2].replace('Type: ', '')}")
    
    # Example 3: Find specific function by name
    print("\n=== Find Function by Name ===")
    func_results = rag.get_function_by_name("calculateTotal", k=1)
    
    if func_results:
        code, score = func_results[0]
        print(f"Found function with score: {score:.3f}")
        lines = code.split('\n')
        print(f"File: {lines[0].replace('File: ', '')}")
        print(f"Language: {lines[1].replace('Language: ', '')}")
        print("Code:")
        code_lines = code.split('Code:\n')[1].split('\n')[:5]
        for line in code_lines:
            print(f"  {line}")
    
    # Example 4: General code search
    print("\n=== General Code Search ===")
    queries = [
        "database connection",
        "email validation",
        "shopping cart",
        "user creation"
    ]
    
    for query in queries:
        results = rag.search_code(query, k=1)
        if results:
            code, score = results[0]
            lines = code.split('\n')
            func_name = lines[3].replace('Name: ', '')
            language = lines[1].replace('Language: ', '')
            print(f"'{query}' -> {func_name} ({language}) [Score: {score:.3f}]")
    
    # Example 5: Code-specific chat (if API key available)
    print("\n=== Code Analysis ===")
    try:
        # This would work if you have an API key configured
        analysis = rag.chat("What authentication methods are implemented in the codebase?")
        print("AI Analysis:", analysis)
    except ValueError as e:
        print("Chat requires API key. Using similarity search instead:")
        auth_funcs = rag.search_code("authentication method implementation", k=2)
        print(f"Found {len(auth_funcs)} authentication-related functions")
        for code, score in auth_funcs:
            lines = code.split('\n')
            print(f"- {lines[3].replace('Name: ', '')} in {lines[1].replace('Language: ', '')}")
    
    print(f"\n=== Codebase Indexing Complete ===")
    print(f"Indexed {rag.get_chunk_count()} code functions from {code_dir}")
    
    # Cleanup
    import shutil
    shutil.rmtree(code_dir)
    print("Cleaned up temporary files")

if __name__ == "__main__":
    main()
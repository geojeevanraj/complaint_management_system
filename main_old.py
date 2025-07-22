from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import hashlib
import csv

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["complaint_system"]

users_collection = db["users"]
complaints_collection = db["complaints"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register User
def register_user(name, email, password, role='user'):
    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": role
    }
    users_collection.insert_one(user)
    print("User registered successfully.")

# Login User
def login_user(email, password):
    user = users_collection.find_one({"email": email, "password": hash_password(password)})
    return user

# Register Complaint
def register_complaint(user_id, category, description):
    complaint = {
        "user_id": ObjectId(user_id),
        "category": category,
        "description": description,
        "status": "Pending",
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    complaints_collection.insert_one(complaint)
    print("Complaint registered successfully.")

# View Complaints (for user)
def view_user_complaints(user_id):
    complaints = complaints_collection.find({"user_id": ObjectId(user_id)})
    for c in complaints:
        print(f"ID: {c['_id']}, Category: {c['category']}, Status: {c['status']}, Description: {c['description']}")

# View All Complaints (admin)
def view_all_complaints():
    complaints = complaints_collection.find()
    for c in complaints:
        user = users_collection.find_one({"_id": c['user_id']})
        print(f"ID: {c['_id']}, User: {user['name']}, Category: {c['category']}, Status: {c['status']}")

# Update Complaint Status (admin)
def update_complaint_status(complaint_id, status):
    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {"status": status}}
    )
    print("Complaint status updated.")

def assign_complaint(complaint_id, staff_id):
    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {"assigned_to": ObjectId(staff_id)}}
    )
    print("Complaint assigned to staff.")

# Staff: View assigned complaints
def view_assigned_complaints(staff_id):
    complaints = complaints_collection.find({"assigned_to": ObjectId(staff_id)})
    for c in complaints:
        print(f"ID: {c['_id']}, Category: {c['category']}, Status: {c['status']}, Description: {c['description']}")

# Staff: Update status of assigned complaint
def update_assigned_complaint_status(staff_id, complaint_id, status):
    result = complaints_collection.update_one(
        {"_id": ObjectId(complaint_id), "assigned_to": ObjectId(staff_id)},
        {"$set": {"status": status}}
    )
    if result.modified_count:
        print("Complaint status updated.")
    else:
        print("Complaint not found or not assigned to you.")

def delete_complaint(complaint_id, user_id=None, is_admin=False):
    query = {"_id": ObjectId(complaint_id)}
    if not is_admin:
        query["user_id"] = ObjectId(user_id)
    result = complaints_collection.delete_one(query)
    if result.deleted_count:
        print("Complaint deleted successfully.")
    else:
        print("Complaint not found or you do not have permission.")

# View Complaint Details
def view_complaint_details(complaint_id):
    complaint = complaints_collection.find_one({"_id": ObjectId(complaint_id)})
    if complaint:
        user = users_collection.find_one({"_id": complaint['user_id']})
        print(f"ID: {complaint['_id']}\nUser: {user['name']}\nCategory: {complaint['category']}\nStatus: {complaint['status']}\nDescription: {complaint['description']}\nCreated At: {complaint['created_at']}")
        if 'assigned_to' in complaint:
            staff = users_collection.find_one({"_id": complaint['assigned_to']})
            print(f"Assigned To: {staff['name']}")
    else:
        print("Complaint not found.")

# List Staff Members
def list_staff():
    staff_members = users_collection.find({"role": "staff"})
    print("Staff Members:")
    for staff in staff_members:
        print(f"ID: {staff['_id']}, Name: {staff['name']}, Email: {staff['email']}")

# Change Password
def change_password(user_id, old_password, new_password):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user and user['password'] == hash_password(old_password):
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hash_password(new_password)}}
        )
        print("Password updated successfully.")
    else:
        print("Old password is incorrect.")

def search_complaints_by_category(user_id=None, category=None, is_admin=False):
    query = {"category": {"$regex": category, "$options": "i"}}
    if user_id and not is_admin:
        query["user_id"] = ObjectId(user_id)
    complaints = complaints_collection.find(query)
    found = False
    for c in complaints:
        found = True
        print(f"ID: {c['_id']}, Category: {c['category']}, Status: {c['status']}, Description: {c['description']}")
    if not found:
        print("No complaints found for this category.")

def view_complaints_by_status(status):
    complaints = complaints_collection.find({"status": status})
    for c in complaints:
        user = users_collection.find_one({"_id": c['user_id']})
        print(f"ID: {c['_id']}, User: {user['name']}, Category: {c['category']}, Description: {c['description']}")

def export_complaints_to_csv(user_id=None, is_admin=False, filename="complaints_export.csv"):
    query = {}
    if user_id and not is_admin:
        query["user_id"] = ObjectId(user_id)
    complaints = complaints_collection.find(query)
    with open(filename, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["_id", "user_id", "category", "description", "status", "created_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in complaints:
            writer.writerow({k: str(c.get(k, "")) for k in fieldnames})
    print(f"Complaints exported to {filename}")

def view_complaint_statistics():
    total = complaints_collection.count_documents({})
    pending = complaints_collection.count_documents({"status": "Pending"})
    in_progress = complaints_collection.count_documents({"status": "In Progress"})
    resolved = complaints_collection.count_documents({"status": "Resolved"})
    print(f"Total: {total}, Pending: {pending}, In Progress: {in_progress}, Resolved: {resolved}")

def add_comment_to_complaint(staff_id, complaint_id, comment):
    complaints_collection.update_one(
        {"_id": ObjectId(complaint_id), "assigned_to": ObjectId(staff_id)},
        {"$push": {"comments": {"staff_id": staff_id, "comment": comment, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}}}
    )
    print("Comment added to complaint.")

def print_user_menu():
    print("\n1. Register Complaint\n2. View My Complaints\n3. View Complaint Details\n4. Delete Complaint\n5. Change Password\n6. Search Complaints by Category\n7. Export My Complaints to CSV\n8. Logout")

def print_admin_menu():
    print("\n1. View All Complaints\n2. Update Complaint Status\n3. Assign Complaint\n4. List Staff\n5. View Complaints by Status\n6. Search Complaints by Category\n7. Export All Complaints to CSV\n8. View Complaint Statistics\n9. Logout")

def print_staff_menu():
    print("\n1. View Assigned Complaints\n2. Update Complaint Status\n3. Add Comment to Complaint\n4. Logout")

# ----------- Console Menu Demo ------------
def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter choice: ").strip()
        
        if choice == '1':
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            role = input("Role (user/admin/staff): ").strip() or 'user'
            register_user(name, email, password, role)
        
        elif choice == '2':
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            user = login_user(email, password)
            
            if user:
                print(f"Welcome {user['name']} ({user['role']})")
                
                if user['role'] == 'user':
                    while True:
                        print_user_menu()
                        u_choice = input("Enter choice: ").strip()
                        if u_choice == '1':
                            category = input("Complaint Category: ").strip()
                            desc = input("Description: ").strip()
                            register_complaint(user['_id'], category, desc)
                        elif u_choice == '2':
                            view_user_complaints(user['_id'])
                        elif u_choice == '3':
                            cid = input("Enter Complaint ID: ").strip()
                            view_complaint_details(cid)
                        elif u_choice == '4':
                            cid = input("Enter Complaint ID to delete: ").strip()
                            delete_complaint(cid, user['_id'])
                        elif u_choice == '5':
                            old_pw = input("Old Password: ").strip()
                            new_pw = input("New Password: ").strip()
                            change_password(user['_id'], old_pw, new_pw)
                        elif u_choice == '6':
                            category = input("Enter category to search: ").strip()
                            search_complaints_by_category(user['_id'], category)
                        elif u_choice == '7':
                            export_complaints_to_csv(user['_id'])
                        elif u_choice == '8':
                            break
                        else:
                            print("Invalid choice.")
                
                elif user['role'] == 'admin':
                    while True:
                        print_admin_menu()
                        a_choice = input("Enter choice: ").strip()
                        if a_choice == '1':
                            view_all_complaints()
                        elif a_choice == '2':
                            cid = input("Enter Complaint ID: ").strip()
                            status = input("Enter new status (Pending/In Progress/Resolved): ").strip()
                            update_complaint_status(cid, status)
                        elif a_choice == '3':
                            cid = input("Enter Complaint ID to assign: ").strip()
                            staff_email = input("Enter staff email to assign: ").strip()
                            staff = users_collection.find_one({"email": staff_email, "role": "staff"})
                            if staff:
                                assign_complaint(cid, staff['_id'])
                            else:
                                print("Staff not found.")
                        elif a_choice == '4':
                            list_staff()
                        elif a_choice == '5':
                            status = input("Enter status to filter (Pending/In Progress/Resolved): ").strip()
                            view_complaints_by_status(status)
                        elif a_choice == '6':
                            category = input("Enter category to search: ").strip()
                            search_complaints_by_category(None, category, is_admin=True)
                        elif a_choice == '7':
                            export_complaints_to_csv(is_admin=True)
                        elif a_choice == '8':
                            view_complaint_statistics()
                        elif a_choice == '9':
                            break
                        else:
                            print("Invalid choice.")

                elif user['role'] == 'staff':
                    while True:
                        print_staff_menu()
                        s_choice = input("Enter choice: ").strip()
                        if s_choice == '1':
                            view_assigned_complaints(user['_id'])
                        elif s_choice == '2':
                            cid = input("Enter Complaint ID: ").strip()
                            status = input("Enter new status (Pending/In Progress/Resolved): ").strip()
                            update_assigned_complaint_status(user['_id'], cid, status)
                        elif s_choice == '3':
                            cid = input("Enter Complaint ID: ").strip()
                            comment = input("Enter your comment: ").strip()
                            add_comment_to_complaint(user['_id'], cid, comment)
                        elif s_choice == '4':
                            break
                        else:
                            print("Invalid choice.")
            else:
                print("Invalid credentials.")
        
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
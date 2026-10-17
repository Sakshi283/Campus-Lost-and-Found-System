from datetime import datetime, timedelta
from database import items_collection

sample_items = [
    {
        "item_name": "Blue College ID Card",
        "category": "ID Card",
        "report_type": "Lost",
        "location": "University Library",
        "status": "Missing",
        "reporter_name": "Aarav Sharma",
        "reporter_email": "aarav@example.com",
        "date_reported": datetime.now() - timedelta(days=1)
    },
    {
        "item_name": "White Wireless Earbuds",
        "category": "Electronics",
        "report_type": "Found",
        "location": "College Cafeteria",
        "status": "Found",
        "reporter_name": "Priya Verma",
        "reporter_email": "priya@example.com",
        "date_reported": datetime.now() - timedelta(days=2)
    },
    {
        "item_name": "Black Water Bottle",
        "category": "Bottle",
        "report_type": "Lost",
        "location": "Sports Ground",
        "status": "Missing",
        "reporter_name": "Rahul Singh",
        "reporter_email": "rahul@example.com",
        "date_reported": datetime.now() - timedelta(days=3)
    },
    {
        "item_name": "Python Programming Book",
        "category": "Books",
        "report_type": "Found",
        "location": "Computer Lab",
        "status": "Found",
        "reporter_name": "Neha Gupta",
        "reporter_email": "neha@example.com",
        "date_reported": datetime.now() - timedelta(days=4)
    },
    {
        "item_name": "Black Backpack",
        "category": "Accessories",
        "report_type": "Lost",
        "location": "Lecture Hall 2",
        "status": "Missing",
        "reporter_name": "Karan Mehta",
        "reporter_email": "karan@example.com",
        "date_reported": datetime.now() - timedelta(days=5)
    },
    {
        "item_name": "Silver House Keys",
        "category": "Keys",
        "report_type": "Found",
        "location": "Parking Area",
        "status": "Claimed",
        "reporter_name": "Simran Kaur",
        "reporter_email": "simran@example.com",
        "date_reported": datetime.now() - timedelta(days=6)
    },
    {
        "item_name": "Brown Leather Wallet",
        "category": "Accessories",
        "report_type": "Lost",
        "location": "College Canteen",
        "status": "Missing",
        "reporter_name": "Rohan Malhotra",
        "reporter_email": "rohan@example.com",
        "date_reported": datetime.now() - timedelta(days=7)
    },
    {
        "item_name": "Scientific Calculator",
        "category": "Electronics",
        "report_type": "Found",
        "location": "Examination Hall",
        "status": "Returned",
        "reporter_name": "Ananya Jain",
        "reporter_email": "ananya@example.com",
        "date_reported": datetime.now() - timedelta(days=8)
    },
    {
        "item_name": "Red Notebook",
        "category": "Books",
        "report_type": "Lost",
        "location": "University Library",
        "status": "Missing",
        "reporter_name": "Vivek Kumar",
        "reporter_email": "vivek@example.com",
        "date_reported": datetime.now() - timedelta(days=9)
    },
    {
        "item_name": "Black Umbrella",
        "category": "Accessories",
        "report_type": "Found",
        "location": "Main Gate",
        "status": "Found",
        "reporter_name": "Isha Sharma",
        "reporter_email": "isha@example.com",
        "date_reported": datetime.now() - timedelta(days=10)
    },
    {
        "item_name": "USB Flash Drive",
        "category": "Electronics",
        "report_type": "Lost",
        "location": "Computer Lab",
        "status": "Missing",
        "reporter_name": "Aditya Verma",
        "reporter_email": "aditya@example.com",
        "date_reported": datetime.now() - timedelta(days=11)
    },
    {
        "item_name": "Chemistry Practical File",
        "category": "Books",
        "report_type": "Found",
        "location": "Science Block",
        "status": "Returned",
        "reporter_name": "Mehak Arora",
        "reporter_email": "mehak@example.com",
        "date_reported": datetime.now() - timedelta(days=12)
    },
    {
        "item_name": "Blue Spectacles Case",
        "category": "Accessories",
        "report_type": "Lost",
        "location": "Lecture Hall 1",
        "status": "Missing",
        "reporter_name": "Yash Patel",
        "reporter_email": "yash@example.com",
        "date_reported": datetime.now() - timedelta(days=13)
    },
    {
        "item_name": "White Phone Charger",
        "category": "Electronics",
        "report_type": "Found",
        "location": "Student Lounge",
        "status": "Found",
        "reporter_name": "Riya Kapoor",
        "reporter_email": "riya@example.com",
        "date_reported": datetime.now() - timedelta(days=14)
    },
    {
        "item_name": "Green Lunch Box",
        "category": "Other",
        "report_type": "Lost",
        "location": "College Canteen",
        "status": "Missing",
        "reporter_name": "Arjun Das",
        "reporter_email": "arjun@example.com",
        "date_reported": datetime.now() - timedelta(days=15)
    },
    {
        "item_name": "Sports Jersey",
        "category": "Clothing",
        "report_type": "Found",
        "location": "Sports Ground",
        "status": "Claimed",
        "reporter_name": "Pooja Yadav",
        "reporter_email": "pooja@example.com",
        "date_reported": datetime.now() - timedelta(days=16)
    },
    {
        "item_name": "Black Hair Clip",
        "category": "Accessories",
        "report_type": "Lost",
        "location": "Girls Common Room",
        "status": "Missing",
        "reporter_name": "Tanya Sethi",
        "reporter_email": "tanya@example.com",
        "date_reported": datetime.now() - timedelta(days=17)
    },
    {
        "item_name": "Engineering Mathematics Textbook",
        "category": "Books",
        "report_type": "Found",
        "location": "University Library",
        "status": "Found",
        "reporter_name": "Manav Bansal",
        "reporter_email": "manav@example.com",
        "date_reported": datetime.now() - timedelta(days=18)
    },
    {
        "item_name": "Grey Hoodie",
        "category": "Clothing",
        "report_type": "Lost",
        "location": "Hostel Common Room",
        "status": "Missing",
        "reporter_name": "Kriti Sharma",
        "reporter_email": "kriti@example.com",
        "date_reported": datetime.now() - timedelta(days=19)
    },
    {
        "item_name": "Wireless Mouse",
        "category": "Electronics",
        "report_type": "Found",
        "location": "Computer Lab",
        "status": "Returned",
        "reporter_name": "Dev Khanna",
        "reporter_email": "dev@example.com",
        "date_reported": datetime.now() - timedelta(days=20)
    },
    {
        "item_name": "Blue Geometry Box",
        "category": "Other",
        "report_type": "Lost",
        "location": "Lecture Hall 3",
        "status": "Missing",
        "reporter_name": "Sana Ali",
        "reporter_email": "sana@example.com",
        "date_reported": datetime.now() - timedelta(days=21)
    }
]

# Insert sample records into MongoDB
result = items_collection.insert_many(sample_items)

print(f"{len(result.inserted_ids)} sample records inserted successfully!")
print("Total records in collection:", items_collection.count_documents({}))
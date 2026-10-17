import re
from datetime import date, datetime

import streamlit as st
from pymongo.errors import PyMongoError
from database import client, db, items_collection, test_connection

st.set_page_config(page_title="Campus Lost & Found", page_icon="🎒", layout="wide")

CATEGORIES = ["ID Card", "Electronics", "Accessories", "Books", "Clothing", "Keys", "Bottle", "Other"]
REPORT_TYPES = ["Lost", "Found"]
STATUSES = ["Missing", "Found", "Claimed", "Returned"]

def valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email.strip()))

def show_connection_status():
    if test_connection():
        st.sidebar.success("MongoDB connected")
    else:
        st.sidebar.error("MongoDB is not reachable")
        st.sidebar.info("Start the MongoDB Server, then refresh this page.")

def item_to_dict(item):
    return {
        "Item": item.get("item_name", ""),
        "Category": item.get("category", ""),
        "Report type": item.get("report_type", ""),
        "Location": item.get("location", ""),
        "Date reported": item.get("date_reported", ""),
        "Status": item.get("status", ""),
        "Reporter": item.get("reporter_name", ""),
        "Description": item.get("description", ""),
        "Email": item.get("reporter_email", ""),
        "ID": str(item.get("_id", "")),
    }

st.title("🎒 Campus Lost & Found Management System")
st.caption("Report, search and track items lost or found around campus.")
show_connection_status()

if not test_connection():
    st.warning("MongoDB se connection nahi ho raha. Make sure MongoDB Server is running.")
    st.stop()

menu = st.sidebar.radio(
    "Choose an option",
    ["Dashboard", "Add Item Report", "View / Search Items", "Update Item", "Delete Item", "Analytics"]
)

if menu == "Dashboard":
    st.subheader("Campus overview")
    total = items_collection.count_documents({})
    lost = items_collection.count_documents({"report_type": "Lost"})
    found = items_collection.count_documents({"report_type": "Found"})
    returned = items_collection.count_documents({"status": "Returned"})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total reports", total)
    c2.metric("Lost reports", lost)
    c3.metric("Found reports", found)
    c4.metric("Returned items", returned)
    st.info("Use the sidebar to submit a report, search records, update statuses, or view aggregation analytics.")
    recent = list(items_collection.find().sort("date_reported", -1).limit(5))
    if recent:
        st.subheader("Recent reports")
        st.dataframe([item_to_dict(x) for x in recent], use_container_width=True, hide_index=True)
    else:
        st.write("No reports yet. Add your first item report.")

elif menu == "Add Item Report":
    st.subheader("Add a lost or found item")
    with st.form("add_item_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Item name *", placeholder="e.g. Black wallet")
            category = st.selectbox("Category *", CATEGORIES)
            report_type = st.selectbox("Report type *", REPORT_TYPES)
            location = st.text_input("Campus location *", placeholder="e.g. University Library")
        with col2:
            report_date = st.date_input("Date lost/found *", value=date.today())
            reporter_name = st.text_input("Your name *")
            reporter_email = st.text_input("Your email *")
            description = st.text_area("Description", placeholder="Describe the item without sharing sensitive information.")
        submitted = st.form_submit_button("Submit report", type="primary")

    if submitted:
        errors = []
        if not item_name.strip():
            errors.append("Item name is required.")
        if not location.strip():
            errors.append("Campus location is required.")
        if not reporter_name.strip():
            errors.append("Reporter name is required.")
        if not valid_email(reporter_email):
            errors.append("Enter a valid email address.")
        if report_date > date.today():
            errors.append("Date lost/found cannot be in the future.")
        if errors:
            for error in errors:
                st.error(error)
        else:
            document = {
                "item_name": item_name.strip(),
                "category": category,
                "report_type": report_type,
                "location": location.strip(),
                "description": description.strip(),
                "status": "Missing" if report_type == "Lost" else "Found",
                "reporter_name": reporter_name.strip(),
                "reporter_email": reporter_email.strip().lower(),
                "date_reported": datetime.combine(report_date, datetime.min.time()),
                "created_at": datetime.now(),
            }
            try:
                result = items_collection.insert_one(document)
                st.success(f"Report added successfully! Report ID: {result.inserted_id}")
            except PyMongoError as exc:
                st.error(f"Could not save the report: {exc}")

elif menu == "View / Search Items":
    st.subheader("View and search reports")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_text = st.text_input("Search item name")
    with col2:
        type_filter = st.selectbox("Report type", ["All"] + REPORT_TYPES)
    with col3:
        category_filter = st.selectbox("Category", ["All"] + CATEGORIES)

    query = {}
    if search_text.strip():
        query["item_name"] = {"$regex": re.escape(search_text.strip()), "$options": "i"}
    if type_filter != "All":
        query["report_type"] = type_filter
    if category_filter != "All":
        query["category"] = category_filter

    records = list(items_collection.find(query).sort("date_reported", -1).limit(500))
    if records:
        st.caption(f"Showing {len(records)} report(s), up to 500.")
        st.dataframe([item_to_dict(x) for x in records], use_container_width=True, hide_index=True)
    else:
        st.info("No matching reports found.")

elif menu == "Update Item":
    st.subheader("Update a report")
    records = list(items_collection.find().sort("date_reported", -1).limit(500))
    if not records:
        st.info("There are no reports to update yet.")
    else:
        labels = {
            str(x["_id"]): f'{x.get("item_name", "Unnamed")} — {x.get("report_type", "")} — {x.get("location", "")} — ID: {x["_id"]}'
            for x in records
        }
        selected_id = st.selectbox("Select report", list(labels.keys()), format_func=lambda x: labels[x])
        selected = next(x for x in records if str(x["_id"]) == selected_id)
        with st.form("update_form"):
            new_status = st.selectbox(
                "Status",
                STATUSES,
                index=STATUSES.index(selected.get("status", "Missing")) if selected.get("status", "Missing") in STATUSES else 0,
            )
            new_location = st.text_input("Location", value=selected.get("location", ""))
            new_description = st.text_area("Description", value=selected.get("description", ""))
            save = st.form_submit_button("Save changes", type="primary")
        if save:
            if not new_location.strip():
                st.error("Location cannot be empty.")
            else:
                try:
                    items_collection.update_one(
                        {"_id": selected["_id"]},
                        {"$set": {
                            "status": new_status,
                            "location": new_location.strip(),
                            "description": new_description.strip(),
                            "updated_at": datetime.now(),
                        }},
                    )
                    st.success("Report updated successfully. Refresh the page if needed.")
                except PyMongoError as exc:
                    st.error(f"Could not update report: {exc}")

elif menu == "Delete Item":
    st.subheader("Delete a report")
    records = list(items_collection.find().sort("date_reported", -1).limit(500))
    if not records:
        st.info("There are no reports to delete.")
    else:
        labels = {
            str(x["_id"]): f'{x.get("item_name", "Unnamed")} — {x.get("report_type", "")} — ID: {x["_id"]}'
            for x in records
        }
        selected_id = st.selectbox("Select report to delete", list(labels.keys()), format_func=lambda x: labels[x])
        confirm = st.checkbox("I understand this permanently deletes the selected report.")
        if st.button("Delete report", type="primary", disabled=not confirm):
            try:
                from bson import ObjectId
                result = items_collection.delete_one({"_id": ObjectId(selected_id)})
                if result.deleted_count:
                    st.success("Report deleted.")
                    st.rerun()
                else:
                    st.warning("Report was not found.")
            except PyMongoError as exc:
                st.error(f"Could not delete report: {exc}")

elif menu == "Analytics":
    st.subheader("MongoDB aggregation analytics")
    st.markdown("These summaries are calculated using MongoDB aggregation pipelines.")
    type_pipeline = [
        {"$group": {"_id": "$report_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    category_pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    status_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    location_pipeline = [
        {"$group": {"_id": "$location", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    try:
        a, b = st.columns(2)
        with a:
            st.write("**Reports by type**")
            st.dataframe(
                [{"Report type": x["_id"], "Count": x["count"]} for x in items_collection.aggregate(type_pipeline)],
                use_container_width=True, hide_index=True,
            )
            st.write("**Reports by status**")
            st.dataframe(
                [{"Status": x["_id"], "Count": x["count"]} for x in items_collection.aggregate(status_pipeline)],
                use_container_width=True, hide_index=True,
            )
        with b:
            st.write("**Reports by category**")
            st.dataframe(
                [{"Category": x["_id"], "Count": x["count"]} for x in items_collection.aggregate(category_pipeline)],
                use_container_width=True, hide_index=True,
            )
            st.write("**Top 5 campus locations**")
            st.dataframe(
                [{"Location": x["_id"], "Count": x["count"]} for x in items_collection.aggregate(location_pipeline)],
                use_container_width=True, hide_index=True,
            )
    except PyMongoError as exc:
        st.error(f"Could not calculate analytics: {exc}")

st.sidebar.divider()
st.sidebar.caption("Academic demo project • Use fictional sample data for testing.")

import tkinter as tk
from tkinter import messagebox
import mysql.connector as connector
import random

class VotingSystem:
    def __init__(self, root): 
        self.root = root
        self.root.title("Collage Voting System") 
        
        self.db = connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='root',
            database='voting_system'
        )
        self.main_menu() 

    def clear_window(self): 
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self): 
        self.clear_window() 

        tk.Label(self.root, text="What do you want to do?", font=("Arial", 16)).pack(pady=10) 
        
        tk.Button(self.root, text="Sign Up", command=self.sign_up, width=20).pack(pady=5) 
        tk.Button(self.root, text="Login", command=self.login, width=20).pack(pady=5) 
        tk.Button(self.root, text="Nomination File", command=self.candidate_registration, width=20).pack(pady=5) 
        tk.Button(self.root, text="View Result", command=self.show_result, width=20).pack(pady=5) 
        tk.Button(self.root, text="Leave", command=self.root.quit, width=20).pack(pady=5) 

    def sign_up(self): 
        self.clear_window() 

        labels = ["University Roll Number:", "Full Name:", "Gender (F/M/Other):","Phone Number:","E-mail Address","Department","Admission Year","Password:", "Confirm Password:"]
        
        entries = [tk.Entry(self.root) for _ in labels]
        
        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            entries[i].grid(row=i, column=1, padx=10, pady=5)

        def submit_sign_up():
            values = [entry.get() for entry in entries]
            RollNo, Name, Sex, Phone, Email, Department, AdmissionYear, Password, Confirm_pass = values

            Name = Name.upper()
            Sex = Sex.upper()
            Department = Department.upper()

            if len(RollNo) != 12 or not RollNo.isnumeric():
                messagebox.showerror("Error", "Invalid University Roll Number!")
                return
            if not Name.isalpha():
                messagebox.showerror("Error", "Name can only contain characters!")
                return
            if Sex not in ['F', 'M', 'OTHER']:
                messagebox.showerror("Error", "Invalid Gender!")
                return
            if len(Phone) != 10 or not Phone.isnumeric():
                messagebox.showerror("Error", "Invalid Phone number!")
                return
            if '@ssipmt.com' not in Email or '.' not in Email:
                messagebox.showerror("Error", "Invalid Email! Please enter SSIPMT collage e-mail id.")
                return
            if Department not in ['CSE','ET&T','IT','AI','AI/ML','CSE(AI)','CIVIL','MECHANICAL']:
                messagebox.showerror("Error", "Invalid Department!")
                return
            if len(AdmissionYear) != 4 or not AdmissionYear.isnumeric():
                messagebox.showerror("Error", "Invalid Admission Year!")
                return
            if len(Password) > 8 or Password != Confirm_pass:
                messagebox.showerror("Error", "Passwords do not match!")
                return

            query = f"INSERT INTO voter_table VALUES ('{RollNo}', '{Name}', '{Sex}', '{Phone}', '{Department}', '{AdmissionYear}', '{Email.lower()}')"
            cur = self.db.cursor()
            cur.execute(query)
            self.db.commit()

            VoterId = self.user_table(RollNo, Name, Sex, Phone, Department, AdmissionYear, Email, Password)
            messagebox.showinfo("Success", f"Registration completed! VoterID: {VoterId}")
            self.main_menu()

        tk.Button(self.root, text="Submit", command=submit_sign_up).grid(row=len(labels), column=1, pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).grid(row=len(labels)+1, column=1, pady=10)

    def user_table(self, RollNo, Name, Sex, Phone, Department, AdmissionYear, Email, Password):
        vid = Name[:2].upper() + str(random.randint(1000001, 9999999))
        query = f"INSERT INTO user_table VALUES ('{vid}', '{RollNo}', '{Password}')"
        cur = self.db.cursor()
        cur.execute(query)
        self.db.commit()
        return vid

    def login(self):
        self.clear_window()

        labels = ["University Roll Number:", "Voter ID:", "Password:"]
        entries = [tk.Entry(self.root) for _ in labels]
        entries[-1].config(show="*")

        for i, label in enumerate(labels):
            tk.Label(self.root, text=label).grid(row=i, column=0, padx=10, pady=5)
            entries[i].grid(row=i, column=1, padx=10, pady=5)

        def submit_login():
            RollNumber, VoterId, Password = [entry.get() for entry in entries]

            query = f"SELECT Password FROM user_table WHERE vid='{VoterId}' AND RollNo='{RollNumber}'"
            try:
                cur = self.db.cursor()
                cur.execute(query)
                result = cur.fetchone()

                if result and Password == result[0]:
                    messagebox.showinfo("Success", "Login successful!")
                    self.after_login(RollNumber)
                else:
                    messagebox.showerror("Error", "Invalid credentials!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred at submit_login: {e}")
            finally:
                cur.close() 

        tk.Button(self.root, text="Login", command=submit_login).grid(row=len(labels), column=1, pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).grid(row=len(labels)+1, column=1, pady=10)

    def after_login(self, RollNo):
        self.clear_window()

        tk.Label(self.root, text="Welcome! Choose an option:", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Vote", command=lambda: self.vote(RollNo), width=20).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.main_menu, width=20).pack(pady=5)

    def vote(self, RollNumber):
        self.clear_window()

        tk.Label(self.root, text="Select a candidate for each position:", font=("Arial", 16)).pack(pady=10)

        candidate_vars = {}
        positions = self.get_positions()

        # Create a section for each position
        for pos in positions:
            position_label = tk.Label(self.root, text=f"Position: {pos[0]}", font=("Arial", 14))
            position_label.pack(pady=5)

            candidate_var = tk.StringVar()
            candidates = self.get_candidates_for_position(pos[1])

            for cand in candidates:
                candidate_button = tk.Radiobutton(self.root, text=cand[0], variable=candidate_var, value=cand[0])
                candidate_button.pack(anchor="w")

            candidate_vars[pos[1]] = candidate_var

        def submit_vote():
            for position_id, candidate_var in candidate_vars.items():
                selected_candidate = candidate_var.get()

                if selected_candidate:
                    # Check if the voter has already voted for this position
                    check_query = f"""
                    SELECT COUNT(*) FROM votes 
                    WHERE RollNo='{RollNumber}' 
                    AND CandidateId IN (
                        SELECT CandidateId FROM candidates WHERE PositionId={position_id}
                    )
                    """
                    cur = self.db.cursor()
                    cur.execute(check_query)
                    already_voted = cur.fetchone()[0]

                    if already_voted:
                        messagebox.showerror("Error", f"You have already voted for the position '{self.get_position_name(position_id)}'.")
                    else:
                        # Insert the vote if they haven't voted for this position
                        insert_query = f"""
                        INSERT INTO votes (RollNo, CandidateId) 
                        VALUES ('{RollNumber}', 
                                (SELECT CandidateId FROM candidates 
                                WHERE CandidateName='{selected_candidate}' 
                                AND PositionId={position_id}))
                        """
                        cur.execute(insert_query)
                        self.db.commit()
                        messagebox.showinfo("Success", f"Vote submitted successfully for the position '{self.get_position_name(position_id)}'.")

            self.main_menu()

        tk.Button(self.root, text="Submit Vote", command=submit_vote).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.main_menu).pack(pady=10)

    def get_positions(self):
        query = "SELECT PositionName, PositionId FROM positions"
        cur = self.db.cursor()
        cur.execute(query)
        return cur.fetchall()

    def get_candidates_for_position(self, position_id):
        query = f"SELECT CandidateName FROM candidates WHERE PositionId={position_id}"
        cur = self.db.cursor()
        cur.execute(query)
        return cur.fetchall()

    def candidate_registration(self):
        self.clear_window()

        labels = ["Candidate Name:", "Position"]
        entries = [tk.Entry(self.root) for _ in labels]

        tk.Label(self.root, text="Position Name:").grid(row=0, column=0, padx=10, pady=5)
        position_entry = tk.Entry(self.root)
        position_entry.grid(row=0, column=1, padx=10, pady=5)
        
        def submit_position():
            position_name = position_entry.get()
            query = f"INSERT INTO positions (PositionName) VALUES ('{position_name}')"
            cur = self.db.cursor()
            cur.execute(query)
            self.db.commit()
            messagebox.showinfo("Success", "Position registered successfully!")
            self.candidate_registration()

        tk.Button(self.root, text="Register Position", command=submit_position).grid(row=1, column=1, pady=10)
        
        tk.Label(self.root, text="Candidate Name:").grid(row=2, column=0, padx=10, pady=5)
        candidate_entry = tk.Entry(self.root)
        candidate_entry.grid(row=2, column=1, padx=10, pady=5)

        def submit_candidate():
            candidate_name = candidate_entry.get()
            position_name = position_var.get()
            
            query = f"SELECT PositionId FROM positions WHERE PositionName='{position_name}'"
            cur = self.db.cursor()
            cur.execute(query)
            position_id = cur.fetchone()[0]

            query = f"INSERT INTO candidates (PositionId, CandidateName) VALUES ({position_id}, '{candidate_name}')"
            cur.execute(query)
            self.db.commit()

            messagebox.showinfo("Success", "Candidate registered successfully!")
            self.candidate_registration()

        tk.Label(self.root, text="Select Position:").grid(row=3, column=0, padx=10, pady=5)
        position_var = tk.StringVar()
        position_menu = tk.OptionMenu(self.root, position_var, *self.get_positions_names())
        position_menu.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Register Candidate", command=submit_candidate).grid(row=4, column=1, pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).grid(row=5, column=1, pady=10)

    def get_position_name(self, position_id):
        query = f"SELECT PositionName FROM positions WHERE PositionId={position_id}"
        cur = self.db.cursor()
        cur.execute(query)
        return cur.fetchone()[0]


    def get_positions_names(self):
        query = "SELECT PositionName FROM positions"
        cur = self.db.cursor()
        cur.execute(query)
        return [pos[0] for pos in cur.fetchall()]

    def show_result(self):
        self.clear_window()

        result_text = tk.Text(self.root)
        result_text.pack(pady=10)

        query = '''
        SELECT p.PositionName, c.CandidateName, COUNT(v.VoteId) AS Votes
        FROM votes v
        JOIN candidates c ON v.CandidateId = c.CandidateId
        JOIN positions p ON c.PositionId = p.PositionId
        GROUP BY p.PositionName, c.CandidateName
        ORDER BY p.PositionName, Votes DESC
        '''
        cur = self.db.cursor()
        cur.execute(query)

        result_text.insert(tk.END, "Position \t\tCandidate \t\tVotes\n")
        result_text.insert(tk.END, "---------------------------------------------\n")
        for position, candidate, votes in cur:
            result_text.insert(tk.END, f"{position}\t\t{candidate}\t\t{votes}\n")

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu).pack(pady=10)

if __name__ == "__main__": 
    root = tk.Tk()
    root.configure(bg="lightblue") 
    app = VotingSystem(root) 
    root.mainloop() 
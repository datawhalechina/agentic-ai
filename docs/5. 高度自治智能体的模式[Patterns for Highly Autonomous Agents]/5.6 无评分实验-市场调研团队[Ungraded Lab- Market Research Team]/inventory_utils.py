import copy
import json
import random

import pandas as pd

from datetime import datetime


def create_inventory_dataframe():
   """
   Create an initial pandas DataFrame containing sunglasses inventory.
   
   Returns:
       pd.DataFrame: A DataFrame with columns for name, item_id, description, 
                    quantity_in_stock, and price for 5 different sunglasses styles.
   """
   # Set seed for reproducible results
   random.seed(42)
   
   # Create the sunglasses inventory data
   sunglasses_data = {
       'name': [
           'Aviator',
           'Wayfarer', 
           'Mystique',
           'Sport',
           'Round'
       ],
       'item_id': ['SG001', 'SG002', 'SG003', 'SG004', 'SG005'],
       'description': [
           'Originally designed for pilots, these teardrop-shaped lenses with thin metal frames offer timeless appeal. The large lenses provide excellent coverage while the lightweight construction ensures comfort during long wear.',
           'Featuring thick, angular frames that make a statement, these sunglasses combine retro charm with modern edge. The rectangular lenses and sturdy acetate construction create a confident look.',
           'Inspired by 1950s glamour, these frames sweep upward at the outer corners to create an elegant, feminine silhouette. The subtle curves and often embellished temples add sophistication to any outfit.',
           'Designed for active lifestyles, these wraparound sunglasses feature a single curved lens that provides maximum coverage and wind protection. The lightweight, flexible frames include rubber grips.',
           'Circular lenses set in minimalist frames create a thoughtful, artistic appearance. These sunglasses evoke a scholarly or creative vibe while remaining effortlessly stylish.'
       ],
       'quantity_in_stock': [
           random.randint(3, 25) for _ in range(5)
       ],
       'price': [
           random.randint(75, 150) for _ in range(5)
       ]
   }
   
   # Create and return the DataFrame
   return pd.DataFrame(sunglasses_data)

import pandas as pd
from datetime import datetime

def create_transaction_dataframe(opening_balance=500.00):
    """
    Create an initial pandas DataFrame for tracking store transactions.
    
    Args:
        opening_balance (float): Starting cash register balance for the day. Defaults to $500.00.
    
    Returns:
        pd.DataFrame: A DataFrame with columns for transaction_id, customer_name, 
                     transaction_summary, transaction_amount, and balance_after_transaction.
                     Includes an initial transaction representing the opening register balance.
    """
    
    # Create the opening balance transaction
    opening_transaction = {
        'transaction_id': ['TXN001'],
        'customer_name': ['OPENING_BALANCE'],
        'transaction_summary': ['Daily opening register balance'],
        'transaction_amount': [opening_balance],
        'balance_after_transaction': [opening_balance]
    }
    
    # Create and return the DataFrame
    return pd.DataFrame(opening_transaction)

# Example usage:
if __name__ == "__main__":
    # Initialize the transaction tracker
    transaction_df = create_transaction_dataframe()
    print("Transaction DataFrame initialized:")
    print(transaction_df)
    print(f"\nCurrent register balance: ${transaction_df['balance_after_transaction'].iloc[-1]:.2f}")

def create_ledger_dataframe():
   """
   Create an empty pandas DataFrame to serve as a sales ledger.
   
   Returns:
       pd.DataFrame: Empty DataFrame with columns for transaction_date, 
                    item_id, quantity, and transaction_type
   """
   return pd.DataFrame(columns=['transaction_date', 'item_id', 'quantity', 'transaction_type'])

def get_formatted_item_names(df):
   """
   List all item names in the inventory database.
   
   This function can be used to find the best matching item name to a natural language description.
   The names returned by this function can be used with other inventory tools like check_stock_by_name() 
   and update_stock().
   
   Args:
       df (pd.DataFrame): The inventory DataFrame
   
   Returns:
       list: A list of all item names in the inventory
   """
   return df['name'].tolist()

def check_inventory_by_name(df, item_name):
   """
   Check if an item is in stock by searching for it by name.
   
   Args:
       df (pd.DataFrame): The inventory DataFrame
       item_name (str): The name of the item to check (case-insensitive)
   
   Returns:
       int: The quantity in stock, or -1 if item not found
   """
   # Convert search term to lowercase for case-insensitive matching
   item_name_lower = item_name.lower()
   
   # Find the item (case-insensitive search)
   matching_items = df[df['name'].str.lower() == item_name_lower]
   
   if matching_items.empty:
       return -1
   
   # Get the quantity from the first matching item
   return matching_items.iloc[0]['quantity_in_stock']

def update_stock(df, item_name, transaction_type, quantity):
   """
   Update the stock quantity for an item based on a transaction.
   
   Args:
       df (pd.DataFrame): The inventory DataFrame
       item_name (str): The name of the item to update (case-insensitive)
       transaction_type (str): Either 'sale' or 'return'
       quantity (int): The quantity to add or subtract (must be > 0)
   
   Returns:
       bool: True if update was successful, False if item not found or invalid input
   """
   # Validate inputs
   if quantity <= 0:
       return False
   
   if transaction_type.lower() not in ['sale', 'return']:
       return False
   
   # Convert search term to lowercase for case-insensitive matching
   item_name_lower = item_name.lower()
   
   # Find the item
   item_mask = df['name'].str.lower() == item_name_lower
   
   if not item_mask.any():
       return False
   
   # Update the quantity based on transaction type
   if transaction_type.lower() == 'sale':
       df.loc[item_mask, 'quantity_in_stock'] -= quantity
   elif transaction_type.lower() == 'return':
       df.loc[item_mask, 'quantity_in_stock'] += quantity
   
   # Ensure quantity doesn't go below 0
   df.loc[item_mask, 'quantity_in_stock'] = df.loc[item_mask, 'quantity_in_stock'].clip(lower=0)
   
   return True

def execute_step(step, inventory_df, available_functions):
    """
    Execute a single step of a plan.
    
    Args:
        step (dict): Single task dictionary with 'task' and 'args' keys
        inventory_df (pd.DataFrame): The inventory DataFrame
        available_functions (dict): Dictionary mapping function names to function objects
    
    Returns:
        Any: Result from the executed task
    """
    task_name = step['task']
    task_args = step['args'].copy()  # Copy to avoid modifying original
    
    # Replace 'inventory_df' string with actual DataFrame
    if 'df' in task_args and task_args['df'] == 'inventory_df':
        task_args['df'] = inventory_df
    
    # Get the function and execute it
    func = available_functions[task_name]
    result = func(**task_args)
    
    return result

def execute_plan(plan, inventory_df, available_functions):
    """
    Execute a plan by running each task sequentially.
    
    Args:
        plan (list): List of task dictionaries with 'task' and 'args' keys
        inventory_df (pd.DataFrame): The inventory DataFrame
        available_functions (dict): Dictionary mapping function names to function objects
    
    Returns:
        list: Results from each executed task
    """
    results = []
    
    for step in plan:
        result = execute_step(step, inventory_df, available_functions)
        results.append(result)
        print(f"Executed {step['task']}: {result}")
    
    return results

import json
import copy

def execute_plan_with_reflection(
        client,
        user_query, 
        context,
        planning_instruction,
        initial_plan, 
        available_functions,
        inventory_df, 
        max_reflections_per_step=2
    ):
    """
    Execute a plan with reflection after each step.
    
    Args:
        user_query: Original user request
        initial_plan: List of task dictionaries
        inventory_df: The inventory DataFrame
        max_reflections_per_step: Max number of reflections allowed per step
    
    Returns:
        List of execution records
    """
    
    current_plan = copy.deepcopy(initial_plan)
    execution_history = []
    
    while current_plan:
        # Get next task
        current_task = current_plan[0]
        remaining_plan = current_plan[1:]
        
        print(f"\n--- Executing: {current_task['task']} ---")
        
        # Execute current task
        try:
            function_to_call = available_functions[current_task['task']]
            
            # Add inventory_df to args if it's expected
            args = copy.deepcopy(current_task['args'])
            if 'df' in args and args['df'] == 'inventory_df':
                args['df'] = inventory_df
            
            result = function_to_call(**args)
            execution_status = "SUCCESS"
            print(f"Result: {result}")
            
        except Exception as e:
            result = str(e)
            execution_status = "FAILED"
            print(f"Failed: {result}")
        
        # Record execution
        execution_record = {
            "task": current_task,
            "result": result,
            "status": execution_status
        }
        execution_history.append(execution_record)
        
        # If there are remaining tasks, do reflection
        if remaining_plan:
            print(f"\n--- Reflecting on remaining {len(remaining_plan)} tasks ---")
            
            reflection_count = 0
            plan_updated = True
            
            while plan_updated and reflection_count < max_reflections_per_step:
                
                # Build reflection prompt
                reflection_prompt = build_reflection_prompt(
                    user_query, execution_history, remaining_plan
                )
                
                # Get LLM reflection
                print(f"Reflection attempt {reflection_count + 1}...")
                llm_response = call_llm_for_reflection(client, context, planning_instruction, reflection_prompt)
                
                if "NO_CHANGES_NEEDED" in llm_response:
                    print("No changes needed to plan")
                    plan_updated = False
                else:
                    # Parse new plan from LLM response
                    new_remaining_plan = extract_plan_from_response(llm_response)
                    
                    if new_remaining_plan and new_remaining_plan != remaining_plan:
                        print(f"Plan updated! New remaining tasks: {len(new_remaining_plan)}")
                        remaining_plan = new_remaining_plan
                        reflection_count += 1
                        
                        # Log the reflection
                        execution_history.append({
                            "task": "REFLECTION",
                            "result": f"Plan updated after step {len(execution_history)}",
                            "status": "PLAN_REVISION"
                        })
                    else:
                        print("No actual changes made to plan")
                        plan_updated = False
        
        # Update current plan for next iteration
        current_plan = remaining_plan
    
    return execution_history

def build_reflection_prompt(user_query, execution_history, remaining_plan):
    """Build the reflection prompt for the LLM."""
    
    history_text = format_execution_history(execution_history)
    
    reflection_prompt = f"""
ORIGINAL REQUEST: {user_query}

EXECUTION HISTORY:
{history_text}

CURRENT REMAINING PLAN:
{json.dumps(remaining_plan, indent=2)}

Based on the execution results above, do any of the remaining planned tasks need to be updated?

Consider:
- Did the last execution reveal information that affects upcoming tasks?
- Are there any parameter mismatches (like incorrect item names)?
- Should any tasks be added, removed, or modified?

If changes are needed, provide a new plan for the remaining tasks.
If no changes needed, respond with "NO_CHANGES_NEEDED"

Use the same format as the original planning instruction:
REASONING: [explain if and why changes are needed]
PLAN: [updated JSON array of remaining tasks, or "NO_CHANGES_NEEDED"]
"""
    
    return reflection_prompt

def format_execution_history(history):
    """Format execution history for display."""
    formatted = ""
    for i, record in enumerate(history):
        if record.get("status") == "PLAN_REVISION":
            formatted += f"Step {i+1}: {record['task']} - {record['result']}\n"
        else:
            formatted += f"Step {i+1}: Called {record['task']['task']} with args {record['task']['args']}\n"
            formatted += f"         Result: {record['result']}\n"
            formatted += f"         Status: {record['status']}\n\n"
    return formatted

def call_llm_for_reflection(client, context, planning_instruction, reflection_prompt):
    """Call LLM for reflection step."""
    
    full_prompt = f"{context}\n{planning_instruction}\n\n{reflection_prompt}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that reflects on task execution and updates plans when needed."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.1,
            max_tokens=2000
        )
        print(response.choices[0].message.content.strip())
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error calling OpenAI API for reflection: {e}")
        return "NO_CHANGES_NEEDED"

def extract_plan_from_response(llm_response):
    """Extract plan from LLM response."""
    try:
        if "PLAN:" in llm_response:
            plan_json = llm_response.split("PLAN:")[1].strip()
            
            # Handle markdown code blocks
            if plan_json.startswith("```json"):
                plan_json = plan_json.strip("```json").strip("```").strip()
            
            plan = json.loads(plan_json)
            return plan
        else:
            return None
            
    except json.JSONDecodeError:
        print(f"Failed to parse reflection response: {llm_response}")
        return None
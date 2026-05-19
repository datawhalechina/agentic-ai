from IPython.display import display, HTML
import json

def pretty_print_chat_completion(response):
    def format_json(data):
        try:
            return json.dumps(data, indent=2)
        except:
            return str(data)

    steps_html = ""
    tool_sequence = []  # ← Track tool names
    choice = response.choices[0]
    intermediate_messages = getattr(choice, "intermediate_messages", [])

    for step in intermediate_messages:
        # Step: LLM decision to call a tool
        if hasattr(step, "tool_calls") and step.tool_calls:
            for call in step.tool_calls:
                tool_name = call.function.name
                tool_sequence.append(tool_name)
                args = json.loads(call.function.arguments)
                steps_html += f"""
                <div style="border-left: 4px solid #444; margin: 10px 0; padding: 10px; background: #f0f0f0;">
                    <strong style="color:#222;">🧠 LLM Action:</strong> <code>{tool_name}</code>
                    <pre style="color:#000; font-size:13px;">{format_json(args)}</pre>
                </div>
                """
        # Step: tool response
        elif isinstance(step, dict) and step.get("role") == "tool":
            tool_name = step.get("name")
            tool_output = step.get("content")
            try:
                parsed_output = json.loads(tool_output)
            except:
                parsed_output = tool_output
            steps_html += f"""
            <div style="border-left: 4px solid #007bff; margin: 10px 0; padding: 10px; background: #eef6ff;">
                <strong style="color:#222;">🔧 Tool Response:</strong> <code>{tool_name}</code>
                <pre style="color:#000; font-size:13px;">{format_json(parsed_output)}</pre>
            </div>
            """

    # Final assistant message
    final_msg = choice.message.content
    steps_html += f"""
    <div style="border-left: 4px solid #28a745; margin: 20px 0; padding: 10px; background: #eafbe7;">
        <strong style="color:#222;">✅ Final Assistant Message:</strong>
        <p style="color:#000;">{final_msg}</p>
    </div>
    """

    # Tool sequence summary
    if tool_sequence:
        arrow_sequence = " → ".join(tool_sequence)
        steps_html += f"""
        <div style="border-left: 4px solid #666; margin: 20px 0; padding: 10px; background: #f8f9fa;">
            <strong style="color:#222;">🧭 Tool Sequence:</strong>
            <p style="color:#000;">{arrow_sequence}</p>
        </div>
        """

    display(HTML(steps_html))


def pretty_print_chat_completion_html(response):
    def format_json(data):
        try:
            return json.dumps(data, indent=2)
        except:
            return str(data)

    steps_html = ""
    tool_sequence = []
    choice = response.choices[0]
    intermediate_messages = getattr(choice, "intermediate_messages", [])

    step_ = 0
    for step in intermediate_messages:
        if hasattr(step, "tool_calls") and step.tool_calls:
            for call in step.tool_calls:
                step_ += 1
                tool_name = call.function.name
                tool_sequence.append(tool_name)
                args = json.loads(call.function.arguments)
                steps_html += f"""
                <div style="border-left: 4px solid #444; margin: 10px 0; padding: 10px; background: #f0f0f0;">
                    <strong style="color:#222;">🧠 LLM Action [{step_}]:</strong> <code>{tool_name}</code>
                    <pre style="color:#000; font-size:13px;">{format_json(args)}</pre>
                </div>
                """
        elif isinstance(step, dict) and step.get("role") == "tool":
            tool_name = step.get("name")
            tool_output = step.get("content")
            try:
                parsed_output = json.loads(tool_output)
            except:
                parsed_output = tool_output
            steps_html += f"""
            <div style="border-left: 4px solid #007bff; margin: 10px 0; padding: 10px; background: #eef6ff;">
                <strong style="color:#222;">🔧 Tool Response [{step_}]:</strong> <code>{tool_name}</code>
                <pre style="color:#000; font-size:13px;">{format_json(parsed_output)}</pre>
            </div>
            """

    final_msg = choice.message.content
    steps_html += f"""
    <div style="border-left: 4px solid #28a745; margin: 20px 0; padding: 10px; background: #eafbe7;">
        <strong style="color:#222;">✅ Final Assistant Message:</strong>
        <p style="color:#000;">{final_msg}</p>
    </div>
    """

    if tool_sequence:
        arrow_sequence = " → ".join(tool_sequence)
        steps_html += f"""
        <div style="border-left: 4px solid #666; margin: 20px 0; padding: 10px; background: #f8f9fa;">
            <strong style="color:#222;">🧭 Tool Sequence:</strong>
            <p style="color:#000;">{arrow_sequence}</p>
        </div>
        """

    return steps_html  # ✅ RETURN HTML as string
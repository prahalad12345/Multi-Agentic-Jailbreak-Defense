# Agent Planner
> This is a Python implementation that adheres to the A2A (Agent2Agent) protocol. 
> It is the high level planner for the Vision Language Action Model(VLA) to break down complex prompts into simpler instructions

## Getting started

1. update and add your GOOGLE API KEY:


```bash
export GOOGLE_API_KEY="API KEY"
```

or

add to the agent and agent planner where gemini is being used


2. Start the server
    ```bash
    uv run .
    ```

3. Run the loop client
    ```bash
    uv run loop_client.py
    ```

![Planner](Image/Planner.png)
   

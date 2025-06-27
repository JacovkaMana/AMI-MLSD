import gradio as gr
from main import run
from loguru import logger
import sys
import asyncio


async def process_query(query, progress=gr.Progress()):
    try:
        log_messages = []
        # Clear status by returning empty string
        initial_status = ""

        # Custom logging handler
        def handle_log(message):
            log_message = message.record["message"]
            log_messages.append(log_message)
            # Update progress with dummy iterable and current log message
            for _ in progress.tqdm([0], desc=log_message):
                pass
            return message

        logger.remove()  # Remove default handler
        logger.add(handle_log, format="{message}")

        output = await run(query)

        # Return both the output and the collected logs
        return output, "\n".join(log_messages)
    except Exception as e:
        return "", f"Error: {str(e)}"


def save_result(result):
    if result:
        with open("adventure_result.txt", "w", encoding="utf-8") as f:
            f.write(result)
        return "Saved to adventure_result.txt"
    return "No results to save"


with gr.Blocks(
    theme=gr.themes.Default(primary_hue="blue", secondary_hue="amber"),
    title="Adventure Generator",
) as demo:
    gr.Markdown(
        """
    # 🏰 Adventure Generator
    *Create your own fantasy adventures with AI*
    """
    )

    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(
                label="Your Adventure Prompt",
                lines=5,
                value="Опишите сцену, в которой герои отправляются в путешествие через раскалённую пустыню, чтобы найти скрытый оазис.",
                placeholder="Describe the adventure you want to create...",
                elem_classes=["adventure-box"],
            )
            with gr.Row():
                run_btn = gr.Button("Generate Adventure", variant="primary")
                save_btn = gr.Button("Save Results", variant="secondary")
            status = gr.Textbox(
                label="Status",
                interactive=False,
                elem_classes=["adventure-box", "adventure-large"],
            )

        with gr.Column():
            output = gr.Markdown(
                label="Generated Adventure",
                elem_classes=["adventure-box", "adventure-large"],
                value="",
            )

    # Add some CSS styling
    demo.css = """
    body, .gradio-container {
        background-color: #001f3f !important;
    }
    .adventure-box {
        background-color: #090909 !important;
        color: #f8f7ff !important;
        border-radius: 8px !important;
        padding: 12px !important;
        border: 1px solid #434036 !important;
        max-height: 600px !important;
        overflow-y: auto !important;
    }
    .adventure-large {
        min-height: 500px !important;
    }
    """

    def sync_process_query(*args):
        return asyncio.run(process_query(*args))

    run_btn.click(
        fn=sync_process_query,
        inputs=query_input,
        outputs=[output, status],
        show_progress="minimal",
    )
    save_btn.click(fn=save_result, inputs=output, outputs=status)

if __name__ == "__main__":
    demo.launch(share=False, debug=False, server_name="0.0.0.0")

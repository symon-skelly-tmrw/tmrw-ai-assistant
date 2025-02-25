import os
import re
import config

def extract_typescript_block(response: str) -> str:
    # 1. Use a regex to find a ```typescript fenced block.
    #    We capture everything between the backticks as a group.
    code_block_regex = re.compile(r"```typescript(.*?)```", re.DOTALL)
    match = code_block_regex.search(response)

    # 2. If found, use that block.
    code_only = match.group(1).strip()

    return code_only

def write_new_test_spec_file(generated_test: str):
    try:
        # 1. Use a regex to find a ```typescript fenced block.
        #    We capture everything between the backticks as a group.
        code_block_regex = re.compile(r"```typescript(.*?)```", re.DOTALL)
        match = code_block_regex.search(generated_test)

        # 2. If found, use that block. Otherwise, fallback to the entire text.
        code_only = match.group(1).strip() if match else generated_test.strip()

        # 3. Prepare file path and write out the code
        file_name = 'MyGeneratedTest.spec.ts'
        out_path = os.path.join(config.TESTS_DIR, file_name)

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(code_only)

        print(f"Test spec created: {out_path}")

    except Exception as err:
        print("Failed to generate test from LLM:", err)

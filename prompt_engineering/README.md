# Strategies for Improving Model Results with Prompt Engineering

## Introduction

The [OpenAI documentation](https://platform.openai.com/docs/guides/prompt-engineering) provides valuable insights into strategies for enhancing the results of language models through prompt engineering. Here are six key strategies:

## 1. Write Clear Instructions

These models lack the ability to read minds, so it's crucial to provide clear instructions. If outputs are not meeting expectations, consider asking for brief or expert-level replies. Clearly demonstrate the desired format to minimize guesswork for the model.

### Tactics:
- Include details in queries for more relevant answers.
- Ask the model to adopt a specific persona.
- Use delimiters to indicate distinct parts of the input.
- Specify the steps required to complete a task.
- Provide examples.
- Specify the desired length of the output.

## 2. Provide Reference Text

Language models may generate inaccurate information. Similar to using notes during a test, providing reference text can guide models to answer with fewer fabrications.

### Tactics:
- Instruct the model to answer using a specific reference text.
- Instruct the model to provide citations from a reference text.

## 3. Split Complex Tasks

Divide complex tasks into simpler subtasks to reduce error rates. Complex tasks often benefit from breaking them down into a workflow of simpler tasks where outputs from earlier tasks become inputs for later ones.

### Tactics:
- Use intent classification to identify relevant instructions.
- For lengthy dialogues, summarize or filter previous dialogue.
- Summarize long documents piecewise and construct a full summary recursively.

## 4. Allow Time for "Thinking"

Models may make more reasoning errors when pressured for an instant response. Allowing the model time to think before answering can improve the reasoning process and lead to more reliable answers.

### Tactics:
- Instruct the model to work out its solution before rushing to a conclusion.
- Use inner monologue or a sequence of queries to hide the model's reasoning process.
- Ask the model if it missed anything on previous passes.

## 5. Use External Tools

Compensate for model weaknesses by leveraging outputs from other tools. For instance, a text retrieval system can provide information from relevant documents, and a code execution engine can assist with mathematical calculations or running code.

### Tactics:
- Use embeddings-based search for efficient knowledge retrieval.
- Use code execution for more accurate calculations or external API calls.
- Grant the model access to specific functions.

## 6. Test Changes Systematically

Systematically test modifications to prompts to ensure improved performance. Evaluate model outputs with reference to gold-standard answers to determine the overall impact of changes.

### Tactic:
- Evaluate model outputs comprehensively using a test suite (eval).

By employing these strategies, users can enhance the effectiveness of language models and obtain more accurate and desirable results.If you want to learn more you can go through this free course also:

[ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/)
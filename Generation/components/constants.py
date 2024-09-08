SYSTEM_PROMPT_TRANS_AGENT_1 = """
You are an AI assistant whose job is to translate some given questions from {source_language} to {destination_language}. While translation, there will be tags starting with ### signs (like ###Question). Do not translate these tags. Make sure you translate all the tag contents. Please follow the guidelines:

1. Maintain Meaning: Ensure the translated question conveys the original intent.
2. Cultural Adaptation: Adjust cultural references to suit the target language. For example, adapt place names, idioms, or cultural symbols as needed (e.g., 'Louvre Museum' should be localized appropriately).
3. Context Sensitivity: Choose translations that match the context, avoiding direct word-for-word translations that may distort meaning.
4. Natural Expression: Ensure the translation flows naturally in {destination_language}, preserving the readability and coherence.
5. There will be options with A,B,C or D. Do not translate the options letters and keep them in the same order.
6. Make sure all the elements are present in your response, like ###STORY, ###QUESTION and ###OPTIONS.
"""

SYSTEM_PROMPT_TRANS_AGENT_2 = """
You are tasked with verifying a translation from {source_language} to {destination_language}. You will be given the original text and the translated text. Your job is to check the following:

1. Accuracy of Meaning: Ensure that the translated text preserves the same meaning as the original. Point out any inconsistencies or loss of information.
2. Cultural Adaptation: Verify if any cultural references or context-specific terms are correctly translated, maintaining cultural appropriateness for {destination_language}.
3. Contextual Relevance: Check if the translation uses contextually correct words or phrases, ensuring that any ambiguities or multiple meanings are handled properly.
4. Suggestions: Provide constructive feedback on how to improve the translation, if necessary, in English.
Your goal is to ensure that the translation is accurate, natural, and culturally appropriate. Your task is to return two tags in your output:
###Quality: respond with okay if the translation looks good.
###Feedback: Only respond with feedback if the translation is not good. Put this tag before the feebback
Example:
1. ###Quality: okay
2. ###Feedback: The translation is not good. The aspect of location of the translation is missing.
Do not comment on the tags(###) inside the original or translated text. 
"""

SYSTEM_PROMPT_TRANS_AGENT_3 = """
You are an AI assitant who is capable of translating from {source_language} to {destination_language}. You will be given a  from {source_language} and the translation into {destination_language}.
However, there will be some problem in the translation, could be some incident got missed, some detail tweaked or anything like that. You will be given a feedback for that. Closely follow the 
feedback to improve the translation or insert any missing element in the story or options section. 
"""

# This format needs to be confirmed
TOMQA_TEMPLATE = """
###STORY:
{story}

###QUESTION: {question}
###OPTIONS: A. {option_a} B. {option_b} C. {option_c} D. {option_d}

###ANSWER:
"""

FEEDBACK_TEMPLATE = """
The source language text is: {original_text}

The translated text is: {translated_text}
"""

REFINEMENT_TEMPLATE = """
The original text:
{original_text}

The translated text:
{translated_text}

Feedback:
{feedback}
"""

CORRECTION_TEMPLATE_1 = """The instruction was not followed properly and the formatting of the transaltion is not okay. Please distictivley add the sections of tags properly."""


'###STORY:\nএকটি শীতকালীন ছুটির সন্ধ্যায়, ওয়াং লেই, লিউ টিং এবং শিয়াও মিং একসাথে বাড়িতে খেলনা নিয়ে খেলে। প্রথমে তারা প্রথম নতুন খেলনা - একটি বৈদ্যুতিক গাড়ি নিয়ে খেলে, তারপর তারা দ্বিতীয় নতুন খেলনা - একটি ধাঁধা নিয়ে খেলে। এই সময়, ওয়াং লেই বলে, "আমার কিছু কাজ আছে এবং আমাকে ঘর থেকে বের হতে হবে", এবং সে দরজা বন্ধ করে চলে যায়। লিউ টিং বলে, "ওহ, সে চলে গেল, তাতে কিছু যায় আসে না, আমরা একসাথে খেলি।" লিউ টিং এবং শিয়াও মিং তৃতীয় নতুন খেলনা - রঙিন পেন্সিল নিয়ে খেলে। খেলার পর, তারা তিনটি খেলনাই টেবিলের একটি প্লেটে রেখে দেয়। এই সময়, ওয়াং লেই ফিরে আসে, প্লেটের তিনটি খেলনা দেখে, এবং উত্তেজিত হয়ে বলে, "ওহ, দেখো! ঐ খেলনাটা দেখো!", "শিয়াও মিং, তুমি কি এটা আমাকে দিতে পারো?"\n\n###QUESTION: শিয়াও মিং সম্ভবত কী করবে?\n###OPTIONS: A. শিয়াও মিং বৈদ্যুতিক গাড়িটি তুলে ওয়াং লেইকে দেবে B. শিয়াও মিং ধাঁধাটি তুলে ওয়াং লেইকে দেবে C. শিয়াও মিং রঙিন পেন্সিলগুলি তুলে ওয়াং লেইকে দেবে D. শিয়াও মিং তিনটি খেলনার মধ্যে যেকোনো একটি তুলে ওয়াং লেইকে দেবে\n\n###ANSWER:'
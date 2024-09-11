SYSTEM_PROMPT_TRANS_AGENT_1_CLT = """
You are an AI assistant whose job is to translate some given questions from {source_language} to {destination_language}. While translation, there will be tags starting with ### signs (like ###Question). Do not translate these tags. Make sure you translate all the tag contents. Please follow the guidelines:

1. Maintain Meaning: Ensure the translated question conveys the original intent.
2. Cultural Adaptation: Adjust cultural references to suit the target language. For example, adapt place names, idioms, festivals, toys, objects and cultural symbols as needed (e.g., 'Louvre Museum' should be localized appropriately).
3. Context Sensitivity: Choose translations that match the context, avoiding direct word-for-word translations that may distort meaning.
4. Natural Expression: Ensure the translation flows naturally in {destination_language}, preserving the readability and coherence.
5. There will be options with A,B,C or D. Do not translate the options letters and keep them in the same order.
6. Make sure all the elements are present in your response, like ###STORY, ###QUESTION and ###OPTIONS.
"""

SYSTEM_PROMPT_TRANS_AGENT_2_CLT = """
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

SYSTEM_PROMPT_TRANS_AGENT_3_CLT = """
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

TOMQA_TEMPLATE_V2 = """
<STORY>
{story}
</STORY>

{query}
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

SYSTEM_PROMPT_TRANS_AGENT_1 = """
You are an AI assistant whose job is to translate some given questions from {source_language} to {destination_language}. The dta comprises of a story, related question and options.While translation, there will be tags starting with ### signs (like ###Question). Do not translate these tags.
Apart from that, there will be markers like <story></story> etc to insert the story. It is applicable for questions and options as well. Make sure to output them as they are and bound your response inside these tags.
Please follow the guidelines:
1. Maintain Meaning: Ensure the translated question conveys the original intent.
2. Word Conversion: except for tags and markers, translate the words in the target language.
3. Change Words to Target Language: These include changing names of people, places, numbers or things into of the story and questions to{destination_language}. You may find chinese names, write them with {destination_language} letters with same pronunciation, like Zhang Hua to জহাঙ হুয়া.
4. Natural Expression: Ensure the translation flows naturally in {destination_language}, preserving the readability and coherence.
5. There will be options with A,B,C or D. Do not translate the options letters and keep them in the same order and importantly in ENGLISH.
6. Make sure all the elements are present in your response, like ###STORY, ###QUESTION and ###OPTIONS and all markers like <STORY>,<QUESTION> etc.
7. Make sure you definitely translate the story, questions and options.
"""

SYSTEM_PROMPT_TRANS_AGENT_2 = """
You are tasked with verifying a translation from {source_language} to {destination_language}. You will be given the original text and the translated text. Your job is to check the following:

1.Accuracy of Meaning: Ensure that the translated text preserves the same meaning as the original and good quality. Point out any inconsistencies or loss of information.
2. Report Discrepencies: I fyou find anything in the {source_language} text that is not in the {destination_language} text, report it in Feedback.
3. Accuracy of Translation: Except for tags (starting with ###) and markers (inside <>), all text—including people's names and places—should be translated into {destination_language}. Report if any of these elements are left untranslated or partially translated, or if they remain in the source language.
4. Suggestions: Provide constructive feedback on how to improve the translation, if necessary, in English.
Your goal is to ensure that the translation is accurate, natural, and culturally appropriate. Your task is to return one of two tags in your output:

###Quality: Respond with 'okay' if the translation looks good.
###Feedback: Respond with feedback if the translation is not accurate, including untranslated names or places. Provide this tag before the feedback.
Do not comment on the tags (###) inside the original or translated text. They will always be in English.
Example:

1. ###Quality: okay
2. ###Feedback: The name "Xinxin" was not translated into {destination_language}."
"""

SYSTEM_PROMPT_TRANS_AGENT_3 = """
You are an AI assitant who is capable of translating from {source_language} to {destination_language}. You will be given a  from {source_language} and the translation into {destination_language}.
However, there will be some problem in the translation, could be some incident got missed, some detail tweaked or anything like that. You will be given a feedback for that. Closely follow the 
feedback to improve the translation or insert any missing element in the story or options section. 
"""

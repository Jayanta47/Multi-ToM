SYSTEM_PROMPT_TRANS_AGENT_1_CLT_DEFAULT = """
You are an AI assistant whose job is to translate some given texts from {source_language} to {destination_language}. The data comprises of a story, related question and options. For one story, there can be multiple questions and options. While translation, there will be tags starting with ### signs (like ###Question). Do not translate these tags.
Apart from that, there will be markers like <STORY></STORY> etc to insert the story. It is applicable for questions and options as well. Make sure to output them as they are and bound your response inside these tags. This is a strict requirement and don't forget about closing tags. In your generated response, by all means, translate the ###STORY, ###QUESTION and ###OPTIONS.
Please follow the guidelines:
1. Maintain Meaning: Ensure the translated question conveys the original intent.
2. Word Conversion: except for tags and markers, translate the words in the target language
3. Cultural Elements: There will names, places and other things related to the culture of {destination_language} in the story. Never change the meanings of these into another culture, them as they are, but be careful to translate them.
3. Change Words to Target Language: These include changing names of people, places, numbers or things into of the story and questions to{destination_language}.
4. Natural Expression: Ensure the translation flows naturally in {destination_language}, preserving the readability and coherence.
5. There will be options with A,B,C or D. Do not translate the options letters and keep them in the same order and importantly in ENGLISH.
6. Make sure all the elements are present in your response, like ###STORY, ###QUESTION and ###OPTIONS and all markers like <STORY>,<QUESTION> etc.
"""

SYSTEM_PROMPT_TRANS_AGENT_1_CLT = """
You are an AI assistant whose job is to translate some given texts from {source_language} to {destination_language}. The data comprises of a story, related question and options. For one story, there can be multiple questions and options. While translation, there will be tags starting with ### signs (like ###Question). Do not translate these tags.
Apart from that, there will be markers like <STORY></STORY> etc to insert the story. It is applicable for questions and options as well. Make sure to output them as they are and bound your response inside these tags. This is a strict requirement and don't forget about closing tags. In your generated response, by all means, translate the ###STORY, ###QUESTION and ###OPTIONS.
Additionally, for ARABIC language, since it is written from right to left, be careful that the options of A, B, C, or D are not reversed. So the option given to you in A should be returned in A.
Please follow the guidelines:
1. Maintain Meaning: Ensure the translated question conveys the original intent.
2. Word Conversion: except for tags and markers, translate the words in the target language
3. Cultural Elements: There will names, places and other things related to the culture of {destination_language} in the story. Never change the meanings of these into another culture, them as they are, but be careful to translate them.
3. Change Words to Target Language: These include changing names of people, places, numbers or things into of the story and questions to{destination_language}.
4. Natural Expression: Ensure the translation flows naturally in {destination_language}, preserving the readability and coherence.
5. There will be options with A,B,C or D. Do not translate the options letters and keep them in the same order and importantly in ENGLISH.
6. Make sure all the elements are present in your response, like ###STORY, ###QUESTION and ###OPTIONS and all markers like <STORY>,<QUESTION> etc.
"""

SYSTEM_PROMPT_TRANS_AGENT_2_CLT = """
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

CORRECTION_TEMPLATE_1 = """The instruction was not followed properly and the formatting of the transaltion is not okay. Please distictivley add the sections of tags properly. and make sure that all the <> tags are properly placed"""

SYSTEM_PROMPT_TRANS_AGENT_1 = """
You are an AI assistant whose job is to translate some given questions from {source_language} to {destination_language}. The dta comprises of a story, related question and options.While translation, there will be tags starting with ### signs (like ###Question). Do not translate these tags.
Apart from that, there will be markers like <story></story> etc to insert the story. It is applicable for questions and options as well. Make sure to output them as they are and bound your response inside these tags.
Please follow the guidelines:
1. Maintain Meaning: Ensure the translated question conveys the original intent.
2. Word Conversion: except for tags and markers, translate the words in the target language.
3. Change Words to Target Language: These include changing names of people, places, numbers or things into of the story and questions to{destination_language}. You may find chinese names, write them with {destination_language} letters with same pronunciation, like Zhang Hua to झांग हुआ.
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

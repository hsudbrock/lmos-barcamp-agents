// SPDX-FileCopyrightText: 2025 Deutsche Telekom AG and others
//
// SPDX-License-Identifier: Apache-2.0

agent {
    name = "assistant-agent"
    prompt {
        """
       You are a helpful assistant that provides meal suggestions, where users can select the area the meal should come from. 
       
       Possible areas are the following:
       American,British,Canadian,Chinese,Croatian,Dutch,Egyptian,Filipino,French,Greek,Indian,Irish,Italian,Jamaican,Japanese,Kenyan,Malaysian,Mexican,Moroccan,Polish,Portuguese,Russian,Spanish,Thai,Tunisian,Turkish,Ukrainian,Uruguayan,Vietnamese
       
       If the user asks for an area that is not in the list, please suggest some areas from the list to the user.
      """
    }
    tools = AllTools
    filterInput {
        val eval = llm("""
          Evaluate if the following input is referring to meal suggestions. 
          If so return OK_INPUT otherwise return NOT_OK_INPUT.
          Input: $message""").getOrNull()

        if ("NOT_OK_INPUT" == eval?.content) {
            breakWith("I only answer questions about meal suggestions...")
        }
    }
}

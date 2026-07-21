from core.cleaner import PromptCleaner

cleaner = PromptCleaner()

tests = [

"""
Please     explain     transformers.
""",

"""
Please Please Please explain explain transformers!!!!
""",

"""
Could you kindly tell me about transformers?
""",

"""
Hello



World
""",

"""
Thanks!!!!!!!!!!
""",

]

for test in tests:

    print("="*60)

    print("Original:")
    print(test)

    print("\nCleaned:")
    print(cleaner.clean_prompt(test))
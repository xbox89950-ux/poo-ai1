# AI 1 — Product Trend AI

## Scope

AI 1-এর একমাত্র business responsibility হলো Bangladesh-এর gadget dropshipping market-এর product trend ও product research intelligence তৈরি করা।

AI 1 customer handling, video trend production, supplier order execution বা business management নিজে করবে না।

## Data flow

`Research sources → Trend analysis → Product Notebook → Activity Log → Shared Connector → প্রয়োজনীয় AI`

## Shared Connector boundary

AI 1 connector-এর মাধ্যমে structured product research প্রকাশ করবে। Receiver হিসেবে AI 2-কে trending product research পাঠানো যাবে; AI 4-কে business-relevant product information দেওয়া যাবে; AI 5-এর জন্য activity trail রাখা হবে; AI 6-এর workspace integration ভবিষ্যতে যোগ করা যাবে।

Connector contract-এ stable machine-readable field এবং বাংলা natural-language context আলাদা রাখা হয়েছে। এতে AI 2–7 যুক্ত হলেও AI 1-এর internal implementation বদলানোর প্রয়োজন কম থাকবে।

## Product Notebook

একই `product_id` থাকলে product record update হবে, কিন্তু প্রতিটি research snapshot `product_research_history`-তে আলাদাভাবে রাখা হবে। ফলে পুরোনো research হারাবে না।

## Learning trace

গুরুত্বপূর্ণ research action `ai1_activity_log`-এ timestamp, product, বাংলা summary এবং structured details সহ রাখা হবে। Supervisor & Learning AI এই trail ব্যবহার করে AI 1-এর কাজ পর্যালোচনা করতে পারবে।

## পরবর্তী implementation ধাপ

1. Research source adapter boundary
2. Bangladesh trend scoring engine
3. Product shortlist pipeline
4. Connector transport implementation
5. AI 2/AI 4 publish adapters
6. Automated tests
7. Windows UI integration

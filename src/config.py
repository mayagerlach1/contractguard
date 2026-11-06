# The six risk types ContractGuard checks for.
# Keys are the names used in our JSON output; "label" matches the CUAD column names;
# "definition" is copied from CUAD_v1_README.txt (The Atticus Project, CC BY 4.0).

RISKS = {
    "uncapped_liability": {
        "label": "Uncapped Liability",
        "definition": 'Is a party’s liability uncapped upon the breach of its obligation in the contract? This also includes uncap liability for a particular type of breach such as IP infringement or breach of confidentiality obligation.',
    },
    "termination_for_convenience": {
        "label": "Termination For Convenience",
        "definition": 'Can a party terminate this contract without cause (solely by giving a notice and allowing a waiting period to expire)?',
    },
    "exclusivity": {
        "label": "Exclusivity",
        "definition": 'Is there an exclusive dealing commitment with the counterparty? This includes a commitment to procure all “requirements” from one party of certain technology, goods, or services or a prohibition on licensing or selling technology, goods or services to third parties, or a prohibition on collaborating or working with other parties), whether during the contract or after the contract ends (or both).',
    },
    "minimum_commitment": {
        "label": "Minimum Commitment",
        "definition": 'Is there a minimum order size or minimum amount or units per-time period that one party must buy from the counterparty under the contract?',
    },
    "ip_ownership_assignment": {
        "label": "Ip Ownership Assignment",
        "definition": 'Does intellectual property created by one party become the property of the counterparty, either per the terms of the contract or upon the occurrence of certain events?',
    },
    "non_compete": {
        "label": "Non-Compete",
        "definition": 'Is there a restriction on the ability of a party to compete with the counterparty or operate in a certain geography or business or technology sector?',
    },
}

# nexus_content.py

NEXUS_DATA = {
    "howto": """🧭 *How to start*

• Create an account at https://app.nexus.xyz or register a CLI node at https://app.nexus.xyz/nodes  
  Docs: https://docs.nexus.xyz/layer-1/testnet/cli-node

1) Connect wallet  
2) Connect social accounts: Google, X and Discord  
3) Start earn points

*FAQ*
• Multiple devices: Supported under one account. You can run multiple browser tabs or machines at once.  
• Web app vs CLI: Web app – easy, browser-based proving. CLI – for advanced setups on dedicated hardware.  
• 3rd-party provers: Allowed, but Nexus doesn’t provide setup/troubleshooting help.  
• Node limits: Max 100 nodes per account, 50 creations/day.
""",

    "vision": """💡 *Vision & Mission*

Layer 1 blockchain for the AI era – a “world supercomputer” powered by user devices (PCs, phones, servers). Anyone can connect at https://app.nexus.xyz and contribute compute power to earn rewards.
- Universal Proof: a single, unified proof that verifies arbitrary computation and acts as a global source of truth.
- Layer 1 for the Age of AI: run decentralized apps, ML, and heavy algorithms verifiably.
""",

    "architecture": """🏗️ *Architecture & Core Components*

*1. Execution Layer – Verifiable Supercomputer*  
Core of Nexus blockchain: runs transactions, smart contracts, updates balances, and ensures validity.

Based on Incrementally Verifiable Computation (IVC) – every computation step generates a proof, enabling:

- Incremental verifiability – each step provable and aggregatable.  
- Global parallelism – workloads split across decentralized nodes.  
- Recursive aggregation – proofs combined into a Universal Proof with constant verification cost.

*Roles:*  
- Delegators – lightweight nodes running zkVM, producing proofs.  
- Orchestrators – manage delegators, aggregate proofs (will become permissionless).  
- Proof Trees/DAG topology – combines local proofs into one global proof.  

Proven in multiple public testnets with millions of nodes.

*2. Consensus Layer – Planetary-scale Consensus*  
Ensures all nodes agree on state; secures and finalizes the Universal Proof.

- Early phase: Tendermint-based, delegated staking.  
- Mid phase: Orchestrator + re-delegator roles, layered security.  
- Later phase: HotStuff-2, adaptive quorum, and probabilistic fork-choice for extreme resilience.

Target: > (256⁴) nodes, $1T+ staked for maximum security.  
Acts as a verifiability oracle, not just a ledger – finalizing both computation and models.  
Incentives for all participants, from retail delegators to orchestrators.

*3. Storage Layer – Planetary-scale Storage (in development)*  
Completes the triad: compute (Execution), consensus (Consensus), and verifiable storage.

Uses hyper-dimensional encoding + Data Availability Sampling (DAS) for efficient, provable data access.

*Phases:*  
- Mainnet S1 – full replication (Ethereum-like).  
- Mainnet S2 – delegated staking for storage orchestrators.  
- Mainnet ∞ – fully sampled, decentralized access.

Target: $100B+ storage staking; cost goal – store 10MB onchain for $0.0000036/year with 1B node resilience.  
Supports AI-era needs: auditable training data, provable model checkpoints, reproducible inference outputs.
""",

    "testnet": """✨ *Testnet III (Launched June 23, 2025)*

• *Duration:* Live until Mainnet launch in Q3. Unlike previous short testnets, it runs for weeks, open to participants worldwide.  
• *Focus:* Security, decentralization, orchestration testing.

*How It Works*  
- Earn Points: Prove via Nexus OS or CLI to get NEX Testnet III Points.  
- Claim Tokens: Points can be converted into NEX Testnet III Tokens.  
- Starting balance is 0 – earn through proving.  
- Nexus OS Wallet shows token balances.

*Historical Data:*  
- Rewards history, including past testnets: https://app.nexus.xyz/rewards

*Network Info:*  
Property     Value  
Chain ID     3940  
Native Token Nexus Token (NEX)  
RPC (HTTP)   https://testnet3.rpc.nexus.xyz  
RPC (WS)     wss://testnet3.rpc.nexus.xyz  
Explorer     https://testnet3.explorer.nexus.xyz  
Faucet       https://faucets.alchemy.com/faucets/nexus-testnet
""",

    "community": """🤝 *Community & Team*

- CEO: Daniel Marin  (https://x.com/danielmarinq)  
- Chief Scientist: Jens Groth (https://x.com/JensGroth16)  
- VP Brand: John Slater (https://x.com/intothefuzz)  
- Chief Strategy Officer: Alex Fowler (https://x.com/alexanderfowler)  
- VP Engineering: Diego Prats (https://x.com/mexitlan)  
- Proof engineer: Tanner Duve (https://x.com/duveZK)  
- Community lead: Bria (https://x.com/briwhoze)  
- Head of Social: crowe (https://x.com/doctorcrowe)

*Initiatives:* VIA, Universal Proof R&D, Camp Nexus
""",

    "events": """📅 *Events & Blog*

- zkVM updates  
- Validator onboarding  
- Community roles & weekly updates  
- Blog: https://blog.nexus.xyz
""",

    "links": """🔗 *Official Links & Social Channels*

• 🌐 Website: https://nexus.xyz  
• 📄 Whitepaper: https://whitepaper.nexus.xyz  
• 📚 Docs: https://docs.nexus.xyz  
• 📝 Blog: https://blog.nexus.xyz  
• 👤 Daniel Marin: https://x.com/danielmarinq  
• 📸 Instagram: https://instagram.com/nexus.laboratories  
• 💬 Discord: https://discord.gg/nexus-xyz  
• 💻 GitHub: via Docs
""",

    "disclaimer": """⚠️ *Disclaimer*

This is not an official TG Nexus bot — it’s built by the community.  

Creator: https://x.com/forotney?s=21
""",
}

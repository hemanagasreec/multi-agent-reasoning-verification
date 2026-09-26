def build_evidence(transaction, agent_results):
    """
    Build structured, traceable evidence records.

    Only primary analysis agents are used as evidence sources.
    This prevents duplicate evidence from Critic and Analyst agents.
    """

    evidence_records = []

    evidence_id = 1

    primary_agents = [
        "Pattern Agent",
        "Risk Agent",
        "History Agent"
    ]

    seen_evidence = set()

    for result in agent_results:

        # Only use primary analysis agents
        if result.agent_name not in primary_agents:
            continue

        for item in result.evidence:

            text = item.lower().strip()

            # Avoid duplicate observations
            normalized_observation = " ".join(
                text.split()
            )

            if normalized_observation in seen_evidence:
                continue

            seen_evidence.add(
                normalized_observation
            )

            # ==========================================
            # IDENTIFY EVIDENCE RULE
            # ==========================================

            if (
                "historical transaction baseline" in text
                or "historical average" in text
                or "x the historical" in text
            ):

                rule = "AMOUNT_ANOMALY"
                source = "Historical transaction database"

            elif "new device" in text:

                rule = "NEW_DEVICE"
                source = "Transaction input"

            elif "unknown location" in text:

                rule = "UNKNOWN_LOCATION"
                source = "Transaction input"

            elif "unusual hours" in text:

                rule = "UNUSUAL_TRANSACTION_TIME"
                source = "Transaction input"

            elif "missing" in text:

                rule = "MISSING_DATA"
                source = "Transaction input"

            else:

                rule = "GENERAL_TRANSACTION_CHECK"
                source = "Agent analysis"

            # ==========================================
            # CREATE STRUCTURED RECORD
            # ==========================================

            evidence_records.append({

                "evidence_id": (
                    f"E{evidence_id:03d}"
                ),

                "agent": result.agent_name,

                "rule": rule,

                "observation": item,

                "source": source,

                "confidence": result.confidence,

                "revision": result.revision

            })

            evidence_id += 1

    return evidence_records

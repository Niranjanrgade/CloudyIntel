graph TD
    A[Start: User Problem] --> B(Architect_Supervisor);
    
    subgraph "Phase 1: Generate"
        B -- Decomposes Problem --> C{Architect Team (Parallel)};
        C --> D[...Architects (Search + RAG)...];
        D --> E[Aggregate Solution];
    end

    E --> F(Validator_Supervisor);

    subgraph "Phase 2: Validate"
        F -- Decomposes Solution --> G{Validator Team (Parallel)};
        G --> H[...Validators (RAG-Only)...];
        H --> I[Aggregate Validation Feedback];
    end

    I --> J{Factual Check Router};
    
    subgraph "Inner Loop (Factual)"
        J -- Has Factual Errors --> B;
    end

    J -- Factually Correct --> K(Pillar_Audit_Supervisor);

    subgraph "Phase 3: Audit"
        K -- Plans Audit --> L{Pillar Auditor Team (Parallel)};
        L --> M[...Auditors (RAG-Only)...];
        M --> N[Aggregate Audit Feedback];
    end

    N --> O{Architectural Check Router};

    subgraph "Outer Loop (Architectural)"
         O -- Has Design Flaws --> B;
    end

    O -- Approved --> P[End: Final Plan];
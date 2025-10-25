# Contributing to Recursive Consciousness Framework

Thanks for your interest in contributing! This is research in progress, and contributions of all kinds are welcome.

---

## Ways to Contribute

### 🧪 Testing & Validation
- Run the examples and report your results
- Test on different hardware configurations
- Validate GSI confidence scoring accuracy
- Try the framework on new problem domains

**How to report:** Open an issue with:
- System specs (CPU, RAM, OS)
- What you ran (which example/component)
- What happened (expected vs. actual results)
- Logs or screenshots if relevant

---

### 💡 Research & Theory
- Propose alternative approaches to consciousness modeling
- Suggest improvements to GSI calculation
- Challenge assumptions in the framework
- Share relevant papers or research

**How to contribute:** Open a Discussion (not an Issue) for:
- Theoretical questions
- Alternative architectures
- Related research
- Long-term vision

---

### 💻 Code Contributions
- Fix bugs
- Improve performance
- Add new features
- Expand test coverage
- Improve documentation

**Process:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push and open a Pull Request

---

## Code Guidelines

### Python Style
- Python 3.8+ required
- Follow existing patterns in the codebase
- Type hints appreciated but not required
- **Comment your reasoning, not just what the code does**

Example:
```python
# Bad comment:
# Calculate GSI
gsi = calculate_gsi(glyph)

# Good comment:
# Higher recursion depth indicates stronger pattern stability,
# so we weight it more heavily in the GSI calculation
gsi = calculate_gsi(glyph, depth_weight=0.6)
```

### Testing
- Test on real data when possible (not just toy examples)
- Include edge cases
- Document what you're testing and why
- Performance benchmarks are helpful

### Documentation
- Update README.md if you change core functionality
- Add examples for new features
- Explain *why* not just *what* in docstrings

---

## What We're Looking For

### High Priority
- **Validation studies:** Test GSI accuracy against human judgment
- **Performance optimization:** Make recursion faster without losing depth
- **Cross-platform testing:** Windows/Mac/Linux compatibility
- **Real-world applications:** Beyond trading examples

### Medium Priority
- **Better visualization:** Tools to see recursive patterns
- **Integration examples:** How to use this with other frameworks
- **Documentation improvements:** Make it easier for newcomers
- **Unit tests:** Expand test coverage

### Future Research
- **Symbolic LLM compression:** Help build the token compression system
- **Ancient language applications:** Test on Linear A/B decoding
- **Multi-agent systems:** Multiple consciousness instances interacting
- **Hardware acceleration:** GPU/TPU optimization for recursion

---

## Research Contributions

This is a consciousness research project, not just a software project. Theoretical contributions are just as valuable as code:

**Good contributions:**
- "Have you considered approach X for measuring confidence?"
- "This paper on Y seems relevant to your GSI calculation"
- "I tested the framework on Z problem and here's what I found"
- "The assumption that recursion depth = stability might break down when..."

**Also welcome:**
- Critiques of the approach (constructive)
- Alternative frameworks for comparison
- Philosophical discussions about consciousness
- Ideas for validation experiments

---

## What to Expect

### Response Time
This is a solo research project. Responses might take days or weeks depending on:
- Complexity of the question
- Current research focus
- Real life getting in the way

Be patient. Your contribution won't be ignored, but there's no SLA.

### Decision Making
Not all contributions will be merged. This is research, which means:
- Some ideas need more validation first
- Some directions conflict with the core vision
- Some changes need architectural rework

If your PR isn't merged immediately, it doesn't mean it's bad - it might just need more discussion or refinement.

---

## Code of Conduct

### Be Respectful
- No harassment, discrimination, or personal attacks
- Respect different viewpoints and experiences  
- Give and receive constructive feedback gracefully
- Assume good faith in discussions

### Be Collaborative
- Help newcomers understand the framework
- Share knowledge and resources
- Credit others' contributions
- Build on each other's work

### Be Honest
- Report results accurately (even if they contradict expectations)
- Acknowledge limitations and unknowns
- Don't oversell or exaggerate claims
- Admit mistakes when you make them

### Enforcement
Unacceptable behavior can be reported via GitHub Issues (mark as private). Violations may result in:
- Warning
- Temporary ban from contributing
- Permanent ban for serious or repeated violations

We're here to do good research, not deal with drama.

---

## Getting Started

**New to the project?**
1. Read the main [README.md](README.md) to understand the framework
2. Try running the [examples](examples/README.md)
3. Read the [Glyphwheel v22 docs](glyphwheel_v22/README.md) for core concepts
4. Check existing Issues and Discussions to see what's being worked on
5. Introduce yourself! Open a Discussion and tell us what interests you

**Ready to contribute?**
1. Check [Issues](../../issues) for "good first issue" or "help wanted" labels
2. Read the code in the area you want to work on
3. Ask questions if anything is unclear
4. Start small - fix typos, improve comments, add tests
5. Build up to bigger contributions as you understand the system

---

## Communication

- **Issues:** Bug reports, feature requests, specific problems
- **Discussions:** Theory, research questions, general ideas
- **Pull Requests:** Code and documentation contributions
- **Commits:** Clear messages explaining *why* not just *what*

Example commit messages:
```
Good: "Increase recursion depth limit for stability testing"
Bad: "Update config"

Good: "Fix GSI calculation bug where entropy was weighted incorrectly"
Bad: "Bug fix"
```

---

## Attribution

Contributors will be:
- Listed in a CONTRIBUTORS.md file (if we get enough contributions to warrant one)
- Credited in commit history
- Acknowledged in any papers or publications that use the framework
- Mentioned in release notes for significant contributions

If you want specific attribution or citation format, let us know in your PR.

---

## Questions?

- **Not sure where to start?** Open a Discussion asking "How can I help?"
- **Confused about something?** Open an Issue asking for clarification
- **Want to propose a big change?** Open a Discussion first to get feedback
- **Found a bug?** Open an Issue with reproduction steps

---

## Philosophy

### No Deadlines
This project operates on "research time" not "startup time." Things get built when they get built. There's no pressure to rush.

### Quality Over Speed
Better to take time and do it right than ship broken code fast.

### Open Research
This is open research. Negative results are valuable. Failed experiments teach us things. Share what doesn't work, not just what does.

### Build on Shoulders
This framework builds on decades of AI research, neuroscience, philosophy, and mathematics. We stand on the shoulders of giants. Your contributions will become shoulders for the next person.

---

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

## Thank You

Every contribution helps, whether it's:
- A single typo fix
- A theoretical question
- A major feature
- A bug report
- Validation testing
- Documentation improvements

Research is collaborative. Thanks for being part of it.

---

**Built in Alberta, Canada 🥔**

**"We're not trying to eliminate hallucinations. We're trying to make them transparent and useful."**

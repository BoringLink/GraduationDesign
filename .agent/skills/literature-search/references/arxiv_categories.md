# arXiv Categories Reference

## Computer Science

### Machine Learning & AI
- **cs.AI** - Artificial Intelligence (general)
- **cs.LG** - Machine Learning (supervised, unsupervised, reinforcement learning)
- **cs.NE** - Neural and Evolutionary Computing (genetic algorithms, neural networks)
- **cs.CL** - Computation and Language (NLP, natural language processing)

### Vision & Graphics
- **cs.CV** - Computer Vision and Pattern Recognition
- **cs.GR** - Graphics (visualization, rendering)

### Systems & Distributed
- **cs.DC** - Distributed, Parallel, and Cluster Computing
- **cs.OS** - Operating Systems
- **cs.AR** - Hardware Architecture

### Software
- **cs.PL** - Programming Languages
- **cs.SE** - Software Engineering
- **cs.DB** - Databases

### Theory & Algorithms
- **cs.DS** - Data Structures and Algorithms
- **cs.CC** - Computational Complexity

### Other CS
- **cs.HC** - Human-Computer Interaction
- **cs.IR** - Information Retrieval

## Physics

- **physics.comp-ph** - Computational Physics
- **physics.data-an** - Data Analysis, Statistics and Probability

## Education

Note: arXiv doesn't have a dedicated education category. Education-related papers often appear in:
- **cs.CY** - Computers and Society (includes educational technology)
- **physics.ed-ph** - Physics Education

## Quantitative Biology

- **q-bio.NC** - Neurons and Cognition (neuroscience, brain-computer interfaces)

## Query Construction Examples

### Single Category
```
cat:cs.AI
```

### Multiple Categories (OR)
```
cat:cs.AI OR cat:cs.LG
```

### Keywords in Title
```
ti:"deep learning"
```

### Keywords in Abstract
```
abs:"neural networks"
```

### Any Field
```
all:"machine learning"
```

### Combined (AND)
```
all:"deep learning" AND cat:cs.AI AND submittedDate:[202001010000 TO 202312312359]
```

## Common Search Patterns

### Recent Papers in a Field
```
cat:cs.CV AND submittedDate:[202401010000 TO 202404212359]
```

### Author Search
```
au:"Yann LeCun"
```

### Title Keywords
```
ti:"transformer" AND ti:"attention"
```

### Year Range Filter (Post-Processing)
arXiv API doesn't support year filtering directly; filter by `submittedDate` instead.

Date format: `YYYYMMDDHHmm` (e.g., `202001010000` = Jan 1, 2020 00:00 UTC)

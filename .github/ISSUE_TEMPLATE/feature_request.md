name: Feature Request
description: Suggest an idea
labels: [enhancement]

body:
  - type: markdown
    attributes:
      value: |
        Thanks for suggesting a feature!
  
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the feature
    validations:
      required: true
  
  - type: textarea
    id: motivation
    attributes:
      label: Motivation
      description: Why should this be added?
    validations:
      required: true

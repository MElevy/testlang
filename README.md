# testlang

The testlang programming language.

No external requirements!!!

## Syntax

### Values

Testlang has multiple data types:
  - Integers are whole numbers
  - Floats decimal numbers
  - Strings are pieces of text, defined with double quotes `"Text here"`. There are no multiline strings yet

### Variables

The syntax to declare a variable is:
<pre>
variableName: value
</pre>

Creating a variable is considered an expression, and returns the value of the expression assigned.

### Math
testlang has no support for parentheses, currently only addition(`+`), subtraction(`-`), division(`/`), and multiplication(`*`) work.

### Code Blocks

testlang supports codeblocks e.g. 
<pre>
{
  ...
}
</pre>

### Keywords

Currently, testlang has only three keywords: `print`, `input`, and `if`

#### print

The print statement is defined as:
<pre>
print value
</pre>

#### input

`input` is an expression, and is used like:
<pre>
variableName: input
</pre>

#### if

The if statement checks if an expression is true, if so, it executes the code block. It's syntax is:
<pre>
if expression {
 ...
}
</pre>

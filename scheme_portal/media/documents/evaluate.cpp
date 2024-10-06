#include "stack.h"
#include <ctype.h>
#include <math.h>

// Program to evaluate postfix expression
class Postfix {
    stack s1;
public:
    Postfix() {
        s1.head = NULL;
    }
    int Precedence(char);
    char* InfixToPostfix(char*);
    int evaluate(char*);
};

int main() {
    Postfix p1;
    int n;
    printf("Enter the size of the Infix expression: ");
    scanf("%d", &n);
    char *data = (char *)malloc(n * sizeof(char));
    int ch;
    while(1){
        printf("1.Enter Infix expression\n2.Convert Infix to Postfix\n3.Evaluate Postfix expression\n4. Exit\nEnter your choice: ");
        scanf("%d", &ch);
        switch(ch){
            case 1:
                printf("Enter the Infix expression: ");
                scanf("%s", data);
                break;
            case 2:
                printf("Postfix expression: %s\n", p1.InfixToPostfix(data));
                break;
            case 3:
                printf("Result: %d\n", p1.evaluate(p1.InfixToPostfix(data)));
                break;
            case 4:
                return 0;
            default:
                printf("Invalid choice\n");
        }
    }
}

//TIME COMPLEXITY: O(1)
int Postfix::Precedence(char c) {
    if (c == '^') {
        return 3;
    } else if (c == '*' || c == '/' || c == '%') {
        return 2;
    } else if (c == '+' || c == '-') {
        return 1;
    } else if (c == '=') {
        return 0;
    }
    return -1;
}

// Convert Infix to Postfix expression TIME COMPLEXITY: O(n)
char* Postfix::InfixToPostfix(char *data) {
    if (!data) {
        printf("No data\n");
        return NULL;
    }
    char *postfix=(char*)malloc(100*sizeof(char));
    int j=0;

    for (int i=0;data[i]!='\0';i++) {
        if (isdigit(data[i])) {
            while (isdigit(data[i])) {
                postfix[j++] = data[i++];
            }
            postfix[j++] = ' ';  
            i--; 
        } 
        else if (data[i]=='(') {
            s1.push(data[i]);
        } 
        else if (data[i]==')') {
            while (!s1.isEmpty() && s1.peek()!='(') {
                postfix[j++]=s1.pop();
            }
            if (!s1.isEmpty()) {
                s1.pop();
            }
        } 
        else {
            while (!s1.isEmpty() && Precedence(data[i])<=Precedence(s1.peek())) {
                if (data[i]=='^'&&s1.peek()=='^') {
                    break;
                }
                postfix[j++]=s1.pop();
            }
            s1.push(data[i]);
        }
    }
    while (!s1.isEmpty()) {
        postfix[j++]=s1.pop();
    }
    postfix[j]='\0';
    return postfix;
}

// Evaluate Postfix expression TIME COMPLEXITY: O(n)
int Postfix::evaluate(char *data) {
    if (!data) {
        printf("No data\n");
        return -1;
    }

    for (int i = 0; data[i] != '\0'; i++) {
        if (isdigit(data[i])) {
            int num = 0;
            while (isdigit(data[i])) {
                num = num * 10 + (data[i++]-'0');  
            }
            s1.push(num);
        } 
        else if (data[i] != ' ') {
            int A = s1.pop();
            int B = s1.pop();
            switch (data[i]) {
                case '+':
                    s1.push(B + A);
                    break;
                case '-':
                    s1.push(B - A);
                    break;
                case '*':
                    s1.push(B * A);
                    break;
                case '/':
                    s1.push(B / A);
                    break;
                case '^':
                    s1.push(pow(B, A));
                    break;
                default:
                    printf("Invalid operator\n");
                    return -1;
            }
        }
    }

    if (!s1.isEmpty()) {
        return s1.pop();
    } else {
        printf("Error: No result found\n");
        return -1;
    }
}

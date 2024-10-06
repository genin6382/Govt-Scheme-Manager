#include "stack.h"

//program to check if parantheses are balanced

class Balancer{
    stack s1;
    public:
        bool check(char *);
};

int main(){
    Balancer b1;
    char data[100];
    int ch;
    while(1){
        printf("1. Check parantheses\n2. Exit\nEnter your choice: ");
        scanf("%d",&ch);
        switch(ch){
            case 1:
                printf("Enter data: ");
                scanf("%s",data);
                if(b1.check(data)){
                    printf("Balanced\n");
                }
                else{
                    printf("Not Balanced\n");
                }
                break;
            case 2:
                return 0;
            default:
                printf("Invalid choice\n");
        }
    }
    return 0;
}

//CHECK IF PARANTHESIS ARE BALANCED , TIME COMPLEXITY: O(n)
bool Balancer::check(char * data){
    if (!data){
        printf("No data\n");
        return false;
    }
    else if(data[0]==')'){
        printf("Invalid parantheses\n");
        return false;
    }
    for(int i=0;data[i]!='\0';i++){
        if(data[i]=='('){
            s1.push(data[i]);
        }
        else if(data[i]==')'){
            if(s1.isEmpty()){
                printf("Invalid parantheses\n");
                return false;
            }
            char c=s1.peek();
            s1.pop();
            if(!(c=='(' && data[i]==')')){
                printf("Parantheses Mismatch\n");
                return false;
            }
        }
    }
    return s1.isEmpty();

}

/*THE TWO DIFFERENT APPROACHES TO SOLVE THIS PROBLEM ARE:
1. USING STACK (OPTIMAL)-> TIME COMPLEXITY: O(n) 
2. USING COUNTER -> TIME COMPLEXITY: O(n) 

->COUNTER BASED APPROACH DOESNT ACCOUNT FOR THE ORDER OF PARANTHESES.
->STACK BASED APPROACH ACCOUNTS FOR THE ORDER OF PARANTHESES AND CAN HANDLE NESTED AND MIXED PARANTHESES.
*/
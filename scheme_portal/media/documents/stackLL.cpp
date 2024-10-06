#include<stdio.h>
#include<stdlib.h>

class stack{
    struct node{
        char data;
        struct node* next;
    };
    struct node* head;
    public:
        stack(){
            head = NULL;
        }
        struct node* createnode(char );
        void display();
        void push(char );
        char pop();
        char peek();
        bool isEmpty();
};

int main(){
    stack s1;
    int ch;
    char data;
    
    while(1){
        printf("1. Push\n2. Pop\n3. Peek\n4. IsEmpty\n5. Display\n6. Exit\nEnter your choice: ");
        scanf("%d",&ch);
        switch(ch){
            case 1:
                printf("Enter data: ");
                scanf(" %c",&data);
                s1.push(data);
                s1.display();
                break;
            case 2:
                data=s1.pop();
                if(data){
                    printf("Popped element: %c\n",data);
                    s1.display();
                }
                break;
            case 3:
                data=s1.peek();
                if(data){
                    printf("Peek element: %c\n",data);
                }
                break;
            case 4:
                if(s1.isEmpty())
                    printf("Stack is empty\n");
                else
                    printf("Stack is not empty\n");
                break;
            case 5:
                s1.display();
                break;
            case 6:
                return 0;
            default:
                printf("Invalid choice\n");
        }
    }
    return 0;
}
//CREATE NODE , TIME COMPLEXITY: O(1)
stack::node* stack::createnode(char data){
    struct node* newnode=(struct node*)malloc(sizeof(struct node));
    newnode->data = data;
    newnode->next = NULL;
    return newnode;
}

//CHECK IF STACK IS EMPTY , TIME COMPLEXITY: O(1)
bool stack::isEmpty(){
    return head==NULL;
}

//PRINT STACK ELEMENTS , TIME COMPLEXITY: O(n)
void stack::display(){
    struct node*temp=head;
    if(isEmpty()){
        printf("Stack is empty\n");
        return;
    }
    printf("%c <--- PEEK",temp->data);
    temp=temp->next;
    while(temp!=NULL){
        printf("\n%c",temp->data);
        temp=temp->next;
    }
    printf("\n");
}

//PUSH ELEMENT INTO STACK , TIME COMPLEXITY: O(1) ,INSERTION AT BEGINNING
void stack::push(char data){
    struct node* newnode=createnode(data);
    if(isEmpty()){
        head=newnode;
        return;
    }
    newnode->next=head;
    head=newnode;
}

//POP ELEMENT FROM STACK , TIME COMPLEXITY: O(1) , DELETION FROM BEGINNING
char stack::pop(){
    if(isEmpty()){
        printf("Stack is empty\n");
        return '\0';
    }
    struct node* temp=head;
    char data=head->data;
    head=head->next;
    free(temp);
    return data;
}

//PEEK ELEMENT FROM STACK , TIME COMPLEXITY: O(1)
char stack::peek(){
    if(isEmpty()){
        printf("Stack is empty\n");
        return '\0';
    }
    return head->data;
}
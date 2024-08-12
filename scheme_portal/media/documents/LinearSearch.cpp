#include<stdio.h>

void linearSearch(int [],int ,int);

int main(){
    int size,key;

    printf("Enter the size of the array: ");
    scanf("%d",&size);

    int arr[size];
    for (int i = 0; i < size; i++){
        printf("Enter the element at index %d: ",i);
        scanf("%d",&arr[i]);
    }

    printf("Enter the key to search: ");
    scanf("%d",&key);
    linearSearch(arr,size,key);
    return 0;
}

void linearSearch(int arr[],int size,int key){
    for(int i=0;i<size;i++){
        if (arr[i]==key){
            printf("Element found at index %d\n",i);
            return;
        }
    }
    printf("Element not found\n");
}
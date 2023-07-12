#include <list>
#include <iostream>
#include <unistd.h>
#include <pthread.h>
#include <iterator>

using namespace std;

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

struct node {
    int id;
    int size;
    int index;

    //Constructor
    node(int id, int s, int i)
        : id(id), size(s), index(i)
    {}
};

class HeapManager {
    private:
        list<node> l;  //heap list
        int totalSize;  //keeps the total size to check the last node
    public:
        int initHeap(int size);
        int myMalloc(int id, int size);
        int myFree(int id, int index);
        void print();
};

int HeapManager::initHeap (int size) {
    pthread_mutex_lock(&lock);

    totalSize = size; 

    //initialize the node
    node n(-1, size, 0);

    //insert to the list
    l.push_back(n);
    this->print();

    pthread_mutex_unlock(&lock);
    return 1;
}

int HeapManager::myMalloc (int id, int size) {
    pthread_mutex_lock(&lock);
    int iSoFar = 0;  //to move the iterator

    for (list<node>::iterator i = this->l.begin(); i!= this->l.end(); ++i){
        iSoFar++;

        //if the current node is free
        if(i->id == -1){

            //allocate the node directly
            if(i->size == size){

                i->id = id;
                cout << "Allocated for thread " << id << endl;
                this->print();
                pthread_mutex_unlock(&lock);
                return i->index;
            }

            //allocate the node and discard the remaining free node
            else if(i->size > size){
    
                int remainingSize = i->size - size;
                int newIndex = i->index + size;
                i->id = id;
                i->size = size;

                node n(-1, remainingSize, newIndex);
                list<node>::iterator it = this->l.begin();
                advance(it, iSoFar);
                this->l.insert(it, n);

                cout << "Allocated for thread " << id << endl;
                this->print();
                pthread_mutex_unlock(&lock);
                return i->index;
            }
        }
    }

    //the free size is not enough
    cout << "Can not allocate, requested size " << size << " for thread " << id << " is bigger than remaining size" << endl;
    this->print();
    pthread_mutex_unlock(&lock);
    return -1;
}

int HeapManager::myFree (int id, int index) {
    pthread_mutex_lock(&lock);

    int iSoFar = 0;
    
    //Freeing the correct node --> make the id -1
    for (list<node>::iterator i = this->l.begin(); i!= this->l.end(); ++i){
        
        iSoFar++;
        list<node>::iterator prev = this->l.begin();
        list<node>::iterator next = this->l.begin();

        if(i->id == id && i->index == index){
            advance(prev, iSoFar-2);
            advance(next, iSoFar);

            //if the node to be deleted is the first node
            if(iSoFar == 1){

                //merge with next node
                if(next->id == -1){
                    int sizeToBeDeleted = next->size;
                    i->id = -1;
                    l.erase(next);
                    i->size += sizeToBeDeleted;
                }
                //no merge
                else{
                    i->id = -1;
                }
            }

            //if the node to be deleted is the last node
            else if(i->size + i->index == totalSize){

                //merge with prev node
                if(prev->id == -1){
                    int sizeToBeDeleted = i->size;
                    l.erase(i);
                    prev->size += sizeToBeDeleted;
                }
                //no merge
                else{
                    i->id = -1;
                }
            }
            //if the node be deleted is in between
            else{
                //merge with prev and next nodes
                if(prev->id == -1 && next->id == -1){
                    int sizeToBeDeleted = next->size + i->size;
                    l.erase(i);
                    l.erase(next);
                    prev->size += sizeToBeDeleted;
                }
                //merge with prev node
                else if(prev->id == -1){
                    int sizeToBeDeleted = i->size;
                    l.erase(i);
                    prev->size += sizeToBeDeleted;
                }
                //merge with next node
                else if(next->id == -1){
                    int sizeToBeDeleted = next->size;
                    i->id = -1;
                    l.erase(next);
                    i->size += sizeToBeDeleted;
                }
                //no merge
                else{
                    i->id = -1;
                }
            }
            cout << "Freed for thread " << id << endl;
            this->print();
            pthread_mutex_unlock(&lock);
            return 1;
        }
    }
    this->print();
    pthread_mutex_unlock(&lock);
    return -1;
}

void HeapManager::print() {
    for (list<node>::iterator i = this->l.begin(); i!= this->l.end(); ++i){
        cout << "[" << i->id << "][" << i->size << "][" << i->index << "]";
        if(i->size + i->index == totalSize)
            cout << endl;
        else
            cout << "---";
    }
}



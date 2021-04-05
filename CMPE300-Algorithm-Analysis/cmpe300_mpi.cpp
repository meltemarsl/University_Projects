//Student Name: Meltem Arslan
//Student Number: 2016400117
//Compile Status: Compiling
//Program Status: Working

// Filename: mpi_hello.cpp
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "mpi.h"
#include <cmath>
#include <limits>
#include <bits/stdc++.h>


using namespace std;
// calculates Manhattan Distance with the feature values of 2 instances v1 and v2
// a is the # of features
double manhattanDistance(double v1[], double v2[], int a ){  //
    double distance=0;
    for(int i =0; i<a; i++){
	 distance += fabs(v1[i]-v2[i]);   	
    }
    return distance;
}

int main(int argc, char *argv[])
{
    int rank;			// rank of the current processor
    int size;			// # of processors
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);		// gets the rank of the current processor
    MPI_Comm_size(MPI_COMM_WORLD, &size);		// gets the # of processors

   
    int P, N, A, M, T;
    int inputarr[4]; 
    FILE *cin = fopen(argv[1], "r");
    fscanf(cin,"%d", &P); // reads # of processors from argument
    fscanf(cin,"%d", &N); // reads # of instances from argument
    fscanf(cin,"%d", &A); // reads # of features from argument
    fscanf(cin,"%d", &M); // reads # of iterations from argument
    fscanf(cin,"%d", &T); // reads resulting number of features from argument
    double slave_data[N*(A+1)];     //initialize 1d array for slave instance values
    double slave_data_2d[N][A+1];   //initialize 2d array for slave instance values
    double preff[N/(P-1)][A+1];   //initialize 2d array for each slave to store its instance values
    if(rank==0){
        int i =0;
        double data;
        while(fscanf(cin, "%lf", &data)==1){
            slave_data[i]=data;        //Master P0 reads instance values from argument
            i++;
        }
        fclose(cin);
    }
    for(int i =0;i< N; i++){
	for(int j=0; j< A+1; j++){
	    slave_data_2d[i][j] = slave_data[i*(A+1) + j]; //converts instance values from 1d array into 2d array
	}
    }
    double slave_data_2d_withp0[N+N/(P-1)][A+1];    
    for(int i =0;i< N/(P-1); i++){
	for(int j=0; j< A+1; j++){
	    slave_data_2d_withp0[i][j] = 0;	//sets the first A+1 instance values to zero to in order to give P0 
	}
    }
    for(int i =0;i< N; i++){
	for(int j=0; j< A+1; j++){
	    slave_data_2d_withp0[i+N/(P-1)][j] = slave_data_2d[i][j];	//copies the instance values to the new 2d array with p0 values 
	}
    }

    // sends data from Master array slave_data_2d_withp0 to preff array on each processor
    MPI_Scatter(slave_data_2d_withp0,(A+1)*N/(P-1),MPI_DOUBLE,preff,(A+1)*N/(P-1),MPI_DOUBLE,0,MPI_COMM_WORLD);
    MPI_Bcast(&M, 1, MPI_INT, 0, MPI_COMM_WORLD); // broadcast
    MPI_Bcast(&T, 1, MPI_INT, 0, MPI_COMM_WORLD); // broadcast
    int returnMaster[T];    //defines the returning array of Master processor
    for(int i =0; i< T; i++){
	returnMaster[i] =0;  //sets all values to zero
    }
    int resultMaster[T*P];   //initializes the last array of P0 to be printed
	if(rank != 0){
	    int i = 0;
	    double W[A]= {};  //define weight array of the features
	    for(int inst =0; inst< M; inst++){


		//finds the nearest hit using manhattan distance
		int hit;
		int row = N/(P-1);
		double minDist = numeric_limits<double>::max();
		for(int i=0; i< row; i++){
		    if((preff[inst][A] == preff[i][A])&&( inst!= i)){
		        if(minDist > manhattanDistance(preff[inst], preff[i], A)){
			    hit =i;		
			    minDist = manhattanDistance(preff[inst], preff[i], A);
	    		}
		    }

		}



		//finds the nearest miss using manhattan distance
		int miss;
		double minDist2 = numeric_limits<double>::max();
		for(int i=0; i< row; i++){
		    if((preff[inst][A] != preff[i][A])&&( inst!= i)){
			if(minDist2 > manhattanDistance(preff[inst], preff[i], A)){
			    miss =i;
			    minDist2 = manhattanDistance(preff[inst], preff[i], A);
			}
	 	    }

		}


		for(int k=0; k< A; k++){ 

		    //finds the maximum value of a feature column k
		    double max = preff[0][k] ;
		    for(int i =1; i< row; i++){
			if(max< preff[i][k]){
			    max = preff[i][k];
			}
		    }


		    //finds the minimum of a feature column k
		    double min = preff[0][k] ;
		    for(int i =1; i< row; i++){
			if(min> preff[i][k]){
			    min = preff[i][k];
			}
		    }

		    //update the weight values according to relief algorithm
		    W[k] = W[k] - (abs(preff[inst][k]-preff[hit][k])/ (max-min))/M + (abs(preff[inst][k]-preff[miss][k])/ (max-min))/M;
		    
		}
	    }

	    vector<pair<double, int>> W_pair;
	    for(int l=0; l< A; l++){
		W_pair.push_back(make_pair(W[l],l));   //pairs weight values with their indexes
	    }
	    sort(W_pair.begin(), W_pair.end());		//sort weight values
	    for(int b= A-1; b> A-1-T; b--){
		returnMaster[A-1-b] = W_pair[b].second;		//declares an array with the index values of the maximum T weights which will be sent P0 
	    }
	    sort(returnMaster, returnMaster + T);   //sorts the array which will be sent P0 
	    cout << "Slave P" << rank << " :";
	    for(int i =0; i<T; i++){
		cout <<" "<<returnMaster[i]<< " ";    //prints the sorted indexes of T maximum weights of the current processor
	    }
	    cout << endl;
	}
    MPI_Barrier(MPI_COMM_WORLD); // waits all processors
    MPI_Gather(returnMaster, T, MPI_INT, resultMaster, T, MPI_INT, 0, MPI_COMM_WORLD);    //sends the index values to master processor(each slave processor)
    if(rank ==0){
	sort(resultMaster, resultMaster + T*P);   //sorts recieved index values 
	cout << "Master P0 : " << resultMaster[T];  //prints the first 
	
	for(int i=T+1; i< T*P; i++){
	   if((resultMaster[i] != resultMaster[i-1])){
		cout << " "<<resultMaster[i];      //prints the index values revieved from the slave processors without dublication.
	   }	
	}
    }
    MPI_Finalize();
    return(0);
}

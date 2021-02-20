#include<math.h>


float **genpoint(float **data_array,float (*func_x)(float),float (*func_y)(float),float a,float b,float step,float x0,float y0)
{
  
  float iter=a;
  int i;
  int data=(b-a)/step;
  for(i=0;i<data;i++){
  data_array[i][0]=(*func_x)(iter)*100+x0;
  data_array[i][1]=(*func_y)(iter)*100+y0;
  iter+=step;

  }
return data_array;
}



float** new2old(float** data_array,int n,float a,float b){
int i;
for(i=0;i<n;i++){

data_array[i][0]+=a;
data_array[i][1]+=b;

}


  return data_array;
}


float** old2new(float** data_array,int n,float a,float b){
int i;
for(i=0;i<n;i++){

data_array[i][0]-=a;
data_array[i][1]-=b;

}


  return data_array;
}












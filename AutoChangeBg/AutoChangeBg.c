#include<stdio.h>
#include<stdlib.h>
#include<dirent.h>
#include<string.h>
#include<random>
#include<vector>
#include<time.h>
#include<unistd.h>
using namespace std;

bool CheckAndModify(char * filename)
{
    int length = strlen(filename);
    for(int i = 0; i <= length; i++)
    {
        if(filename[i]==' ')
        {
            for(int j = length+1; j > i; j--)
            {
                filename[j] = filename[j-1]; 
            }
            filename[i]='\\';
            i++;length++;
        }
    }
}

int main(int argc, char** argv)
{
    if(argv[1]==NULL)
    {
        printf("Please input Wallpaper Folder.");
        return 0;
    }
    int sleeptime;
    if(argv[2]!=NULL)
    {
        sleeptime = atoi(argv[2]);
        if(sleeptime==0)
        {
            printf("Please set a resonable sleeptime.");
            return 0;
        }
    }
    else
    {
        sleeptime = 600;
    }
    DIR *dir; struct dirent *ptr;
    dir = opendir(argv[1]);
    vector<char*> filename;
    int count =1;
    while((ptr=readdir(dir))!=NULL)
	{
		int length= strlen(ptr->d_name);
		if(length>4)
		{
			for(int i = 0;i<=length-4;i++)
			{
                if((ptr->d_name[i]=='.'&&ptr->d_name[i+1]=='j'&&ptr->d_name[i+2]=='p'&&ptr->d_name[i+3]=='g')
                ||(ptr->d_name[i]=='.'&&ptr->d_name[i+1]=='p'&&ptr->d_name[i+2]=='n'&&ptr->d_name[i+3]=='g'))
				{
                    CheckAndModify(ptr->d_name);
                    filename.push_back(ptr->d_name);
				}
			}
        }
    }
    int num;
    while(1)
    {
        char filepath[250]="";
        char exec[300]="";
        srand((unsigned)time(NULL));
        num = rand()%filename.size();
        strcat(filepath,argv[1]);
        strcat(filepath,"/");
        strcat(filepath,filename[num]);
        printf("%s\n%s\n",filename[num],filepath);
        strcat(exec, "feh --bg-scale ");
        strcat(exec, filepath);
        system(exec);
        sleep(sleeptime);
    }
    return 1;
}

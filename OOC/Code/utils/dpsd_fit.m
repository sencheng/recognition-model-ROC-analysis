clear all
clc
roc_startup
path=pwd;
% idcs=strfind(current_path, '/');
% path=current_path(1:idcs(end-1));
%TITLE=importdata("title.txt");
TITLE = fileread(strcat(path,'/Code/utils/simID.txt')); 
% TITLE='05-22_16:37:40'%# returns a char vector
disp(TITLE)
file_path=strcat(path,'/Data/ByID/',TITLE);
log=readtable(strcat(file_path,'/Matlab/log_',TITLE,'.csv'));
try length(log.N_pat{1})>4
    N=(log.N_pat{1});%{;%num2cell(importdata(strcat("N_pat",TITLE,".txt")));
    N=strsplit(N);
catch
   N={log.N_pat(~isnan(log.N_pat))};%{;%num2cell(importdata(strcat("N_pat",TITLE,".txt")));
   N=num2cell(N{1});
end

% cond=log.cond(~cellfun('isempty',log.cond));%importdata(strcat("cond",TITLE,".txt"));
%N={'25','50','75'};
pat_sep=log.pat_sep;

try
    olp=log.olap(~cellfun('isempty',log.olap));
    olp=strsplit(olp{1});
catch
    olp={log.olap(~isnan(log.olap))};
end
fit='-LL';
rocData=cell(length(pat_sep),length(olp));
for n=1:length(N)
    count=0;
    for i=1:length(pat_sep)
        save_data=struct('R',0,'F', 0,'auc',0);
        save_data.roc_hit={};
        save_data.roc_fa={};
        save_data.zroc_hit={};
        save_data.zroc_fa={};
        for ii=1:length(olp)
            count=count+1;
            progress=count*100/(length(pat_sep)*length(olp));
            try
               title=strcat(file_path,'/Matlab/Model_input/', num2str(N{n}), '_',num2str(pat_sep(i),'%0.1f'),'_',num2str(olp{ii}),'.csv');
               display(title)
               data=roc_import_data(title);
               sep=num2str(pat_sep(i),'%0.1f');
            catch 
               title=strcat(file_path,'/Matlab/Model_input/', num2str(N{n}), '_',num2str(pat_sep(i),'%0.2f'),'_',num2str(olp{ii}),'.csv');
               data=roc_import_data(title);
               sep=num2str(pat_sep(i),'%0.2f');
            end

            data=data{1};
            title1=strcat(file_path,'/Matlab/Model_output/', num2str(N{n}),'_',sep);
            
            range=size(data.luref);
            range=range(1);
            fitStat=fit;
            model='dpsd';
            targf1=data.targf(:,[1:1:size(data.targf,2)-1]);
            luref1=data.luref(:,[1:1:size(data.luref,2)-1]);

            [nConds,nBins]=size(targf1);
            parNames={'Ro','Rn','F'};
            [x0,LB,UB]=gen_pars(model,nBins,nConds,parNames);
%             UB(:,3)=1.5
%             UB(:,2)=0.2
%             LB(:,2)=0.2
%             X0(:,2)=0.2
            
            modelNotes='Full Model';
%             constrfun = @dpsd_sym_constr;


            rocdata=roc_solver1(targf1,luref1,model,fitStat,x0,LB,UB,'notes',modelNotes,'title',title1);
%             param=rocdata;
            rocData{i,ii}=rocdata;
            if ii>1
                save_data.R=[save_data.R,rocdata.dpsd_model.parameters.Ro];
                save_data.F=[save_data.F,rocdata.dpsd_model.parameters.F];
                save_data.auc=[save_data.auc,rocdata.observed_data.accuracy_measures.auc];
            else
                save_data.R=rocdata.dpsd_model.parameters.Ro;
                save_data.F=rocdata.dpsd_model.parameters.F;
                save_data.auc=rocdata.observed_data.accuracy_measures.auc;
            end
            save_data.roc_hit{end+1}=rocdata.dpsd_model.predicted_rocs.roc.target.';
            save_data.zroc_hit{end+1}=rocdata.dpsd_model.predicted_rocs.zroc.target.';
            save_data.roc_fa{end+1}=rocdata.dpsd_model.predicted_rocs.roc.lure.';
            save_data.zroc_fa{end+1}=rocdata.dpsd_model.predicted_rocs.zroc.lure.';
            save_data
            %rocs=rocData.dpsd_model.predicted_rocs
            %save(strcat(path,'/Model_data/Params/',title(1:end-4),'.mat'), 'param')
        save(strcat(title1,'.mat'), 'save_data')
        disp(['Completed ', num2str(ceil(progress)), '%'])

        end
    end
end



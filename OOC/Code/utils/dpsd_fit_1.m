clear all
clc
fit_cond={'Rn:0'};
for ff=1:length(fit_cond)
    notes=fit_cond{ff}
    roc_startup
    cd ../
    path=pwd
    TITLE = fileread(strcat(path,'/Code/utils/simID.txt')); 
    TITLE='12-17_15:25:03'
    disp(TITLE)
    file_path=strcat(path,'/Data/',TITLE);
    fit='-LL';
    try
        subdirectories = extractfield(dir(file_path),'name');
        subdirectories(ismember(subdirectories,{'.','..'})) = [];
    catch
        subdirectories={file_path}
    end
%     subdirectories=file_path; for old simulations

    for dir_ind=1:length(subdirectories)
        try length(subdirectories)>1
            current_directory=strcat(file_path,'/',subdirectories{dir_ind});
        catch
            current_directory=file_path;
        end
        files=dir(fullfile(strcat(current_directory,'/Matlab/Model_input'), '*.csv'));
        files=extractfield(files,'name');
        

        begin={};
        ending={};
        for i=1:length(files)
            info=regexp(files(i),'\_','split');
            begin=[begin,info{1}{1}];
            ending=[ending,info{1}{2}];
        end
        base=unique(begin);
        olap=unique(ending);
        rocData=cell(length(base),length(olap));

        count=0;

        for i=1:length(base)
            save_data=struct('R',0,'F', 0,'auc',0,'hits',0,'fa',0,'fit',0);
            save_data.roc_hit={};
            save_data.roc_fa={};
            save_data.zroc_hit={};
            save_data.zroc_fa={};
            save_data.hits={};
            save_data.fa={};
            save_data.fit={};
            for ii=1:length(olap)
                count=count+1;
                progress=count*100/(length(base)*length(olap));
                title=strcat(current_directory,'/Matlab/Model_input/',base(i),'_',olap(ii));
                data=roc_import_data(title{1});
                data=data{1};
                title1=strcat(current_directory,'/Matlab/Model_output/',notes,'/',base(i));
                title1=title1{1};
                if ~exist(strcat(current_directory,'/Matlab/Model_output/',notes,'/'), 'dir')
                   mkdir(strcat(current_directory,'/Matlab/Model_output/',notes,'/'))
                end

                range=size(data.luref);
                range=range(1);
                fitStat=fit;
                model='dpsd';
                targf1=data.targf;%(:,[1:1:size(data.targf,2)-1]);
                luref1=data.luref;%(:,[1:1:size(data.luref,2)-1]);

                [nConds,nBins]=size(targf1);
                parNames={'Ro','Rn','F'};
                [x0,LB,UB]=gen_pars(model,nBins,nConds,parNames);
                if notes=='Rn:0'
                    UB(:,2)=0.;
                    LB(:,2)=0.;
                    X0(:,2)=0.;
                end
                if notes=='Full'
                    UB(:,3)=0;
                    LB(:,3)=0;
                    X0(:,3)=0;
                end
                modelNotes=notes;
                if notes=='Symm'
                    constrfun = @dpsd_sym_constr;
                    rocdata=roc_solver1(targf1,luref1,model,fitStat,x0,LB,UB,'notes',modelNotes,'constrfun',constrfun,'title',title1);
                else
                    rocdata=roc_solver1(targf1,luref1,model,fitStat,x0,LB,UB,'notes',modelNotes,'title',title1);

                end


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
                save_data.hits{end+1}=rocdata.observed_data.target.cumulative;
                save_data.fa{end+1}=rocdata.observed_data.lure.cumulative;
                save_data.fit{end+1}=rocdata.dpsd_model.fit_statistics;
                save_data
                    %rocs=rocData.dpsd_model.predicted_rocs
                    %save(strcat(path,'/Model_data/Params/',title(1:end-4),'.mat'), 'param')
            save(strcat(title1,'.mat'), 'save_data')
            disp(['Completed ', num2str(ceil(progress)), '%'])
            end
        end
        end
end

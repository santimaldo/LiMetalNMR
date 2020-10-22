function [res ph0]=sm_AutoPhase(S,ZF,pres,method)

angle=(0:1:360/pres)*pres;

switch method
    case{'MaxIntReSpec'}
        Szf=[S ; zeros(ZF-length(S),1)];
        Szf(1,1)=Szf(1,1)/2;
        Spec=fftshift(fft(Szf));
        for i=1:length(angle)
            Sp_try=Spec.*exp(-1i*angle(1,i)*pi/180);
            IntReSpec(1,i)=sum(real(Sp_try(:,1)));
        end
        [~,indice]=max((IntReSpec));
        
        if IntReSpec(1,indice)<0
            angulo=angle(1,indice)-180;
        else
            angulo=angle(1,indice);
        end
          
        
    case{'MinIntImagSpec'}
        Szf=[S ; zeros(ZF-length(S),1)];
        Szf(1,1)=Szf(1,1)/2;
        Spec=fftshift(fft(Szf));
        for i=1:length(angle)
            Sp_try=Spec.*exp(-1i*angle(1,i)*pi/180);
            IntImagSpec(1,i)=sum(imag(Sp_try(1,:)));
        end
        [~,indice]=min(abs(IntImagSpec));
        
        
        angulo=angle(1,indice)
%         if  angle(1,indice)>90
%             angulo=angle(1,indice)-180
%         else
%             angulo=angle(1,indice)
%         end
%         res=S.*exp(-1i*angle(1,indice)*pi/180);
        
            
        
    case{'MinIntImagFID'}
        
        for i=1:length(angle)
            FID_try=S.*exp(-1i*angle(1,i)*pi/180);
            IntImagFID(1,i)=sum(imag(FID_try(1,:)));
        end
        
        [~,indice]=min(abs(IntImagFID));
        if  angle(1,indice)>90
            angulo=angle(1,indice)-180
        else
            angulo=angle(1,indice)
        end
        
    case{'PHIP'}
        
        Szf=[S ; zeros(ZF-length(S),1)];
        Szf(1,1)=Szf(1,1)/2;
        Spec=fftshift(fft(Szf));
        algo=(1:length(Spec));
        
        for i=1:length(angle)
            Sp_try=Spec.*exp(-1i*angle(1,i)*pi/180);
            
            %             x1=(9020:9180)';
            %             y1=real(Sp_try(9020:9180));
            %             p1 = polyfit(x1,y1,1);
            %             x2=(9480:10000)';
            %             y2=real(Sp_try(9480:10000));
            %             p2 = polyfit(x2,y2,1);
            %             IntReSpec(1,i)=abs(p1(1)) + abs(p2(1));
            %
            IntReSpec(1,i)=sum(abs(real(Sp_try(8500:8760))))+sum(abs(real(Sp_try(9580:9900))));
        end
        
        [~,indice]=min(IntReSpec);
        
        if angle(1,indice)>90
            angulo=angle(1,indice)-180
        else
            angulo=angle(1,indice)
        end
        
        
    case{'PHIPlin4'}
        
        Szf=[S ; zeros(ZF-length(S),1)];
        Szf(1,1)=Szf(1,1)/2;
        Spec=fftshift(fft(Szf));
        algo=(1:length(Spec));
        
        for i=1:length(angle)
            Sp_try=Spec.*exp(-1i*angle(1,i)*pi/180);
            
            x1=(1800:1850)';
            y1=real(Sp_try(1800:1850));
            p1 = polyfit(x1,y1,1);
            
            x2=(2020:2100)';
            y2=real(Sp_try(2020:2100));
            p2 =  polyfit(x2,y2,1);
            
            
            IntReSpec(1,i)= abs(p2(1))+abs(p1(1));
            
            a1(i)=p1(1);
            a2(i)=p2(1);
            
        end
        
        %     figure,plot(abs(a1))
        %     oplot(abs(a2))
        %     oplot(IntReSpec)
        
        [mmmmm,indice]=min(IntReSpec);
        
        if angle(1,indice)>90
            angulo=angle(1,indice)-180+0.1
        else
            angulo=angle(1,indice)
        end
        
        
    case{'PHIPlin5'}
        
        Szf=[S ; zeros(ZF-length(S),1)];
        Szf(1,1)=Szf(1,1)/2;
        Spec=fftshift(fft(Szf));
        algo=(1:length(Spec));
        
        for i=1:length(angle)
            Sp_try=Spec.*exp(-1i*angle(1,i)*pi/180);
            
            x2=(8550:8800)';
            y2=real(Sp_try(x2));
            p2 = polyfit(x2,y2,1);
            
            x1=(6500:6900)';
            y1=real(Sp_try(x1));
            p1 =   polyfit(x1,y1,1);
            
            IntReSpec(1,i)= abs(p2(1)) + abs(p1(1));
            
        end
        
        [~,indice]=min(IntReSpec);
        
        if angle(1,indice)>90
            angulo=angle(1,indice)-180+0.1
        else
            angulo=angle(1,indice)
        end
        
        
end
res=S.*exp(-1i*angulo*pi/180);
ph0 = angulo;
end
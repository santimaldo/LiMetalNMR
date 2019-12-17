function Vol_Sens = VolumenSensitivo(Obj, n)
 
    [Ny,Nx,Nz] = size(Obj);

    Vol_Sens = zeros(Ny,Nx,Nz); 
    
    
%     for kk=2:Nz-1
%         for ii=2:Nx-1 
%             for jj=2:Ny-1
%                 if Obj(jj,ii,kk) == 1
%                     if  (Obj(jj,ii+1,kk)==0 || Obj(jj,ii-1,kk)==0)
%                         Vol_Sens(jj,ii,kk)=1;   
% %                                 --------EFECTO DE B1---------
% %                       Comentando ls lineas "B1", elimino la cara perpendicular a B1
% %                       del vol sens. Recordemos que B1 tiene solo componente
% %                       j versor. 
%                     elseif Obj(jj+1,ii,kk)==0 || Obj(jj-1,ii,kk)==0        % "B1"
%                         Vol_Sens(jj,ii,kk)=1;                              % "B1"
%                     elseif Obj(jj,ii,kk+1)==0 || Obj(jj,ii,kk-1)==0        % "B1"
%                         Vol_Sens(jj,ii,kk)=1;                              % "B1"
%                     end
%                 end
%             end
%         end
%      end



v1 = circshift(Obj, n, 1);
v2 = circshift(Obj, -n, 1);
v3 = circshift(Obj, n, 2);
v4 = circshift(Obj, -n, 2);
v5 = circshift(Obj, n, 3);
v6 = circshift(Obj, -n, 3);

Vol_Sens = Obj - v1.*v2.*v3.*v4.*v5.*v6;

end
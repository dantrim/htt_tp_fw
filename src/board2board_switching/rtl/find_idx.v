module find_idx 
   (
    input logic [3:0] in,
    output logic [3:0] out
    );

   always_comb
     begin
	if(in[0])
	  out = 0;
	else if(in[1])
	  out = 1;
	else if(in[2])
	  out = 2;
	else
	  out = 3;
     end
endmodule



module max_fifo_by_flag    (
    
			      input logic [3:0]  evt_available,
			      input logic [3:0]  fifo_group_rd_idx,
			      output logic [2:0] fifo_idx			    
    );

   logic [3:0] 					 valid_fifo;
   
   assign valid_fifo = evt_available & fifo_group_rd_idx;
   
   always_comb
     begin
	 if(valid_fifo  == 0)
	   begin
	      fifo_idx = 4;
	   end
	 else if(valid_fifo[0])
	   fifo_idx = 0;
	 else if(valid_fifo[1])
	   fifo_idx = 1;
	 else if(valid_fifo[2])
	   fifo_idx = 2;
	 else
	   fifo_idx = 3;
     end // always_comb
   
endmodule // group_fifo_by_flag


module sort_fifo_by_rd_count #(parameter FIFO_DEPTH_BITS = 6,
			       parameter TOTAL_CLUSTERS  = 4,
			       parameter TOTAL_FIFO_GROUPS = 1
			       )
   (
    input logic 		      clk,
    input logic 		      rst_n,
    input logic 		      srst_n,
    input logic [FIFO_DEPTH_BITS : 0] fifo_rd_count[TOTAL_CLUSTERS],
    output logic [3:0] 		      fifo_groups[TOTAL_FIFO_GROUPS][5]  
    );

   genvar 			      i,j;
   
   logic [FIFO_DEPTH_BITS : 0] 	      local_fifo_rd_count[TOTAL_FIFO_GROUPS*4];
   logic [FIFO_DEPTH_BITS : 0] 	      fifo_rd_count_4[TOTAL_FIFO_GROUPS][4];
   
   generate
      begin : sort_fifo_by_rd_count_gen
	 for(i=0;i<TOTAL_FIFO_GROUPS*4;i++)
	   begin
	      if(i < TOTAL_CLUSTERS)
		assign local_fifo_rd_count[i] = fifo_rd_count[i];
	      else
		assign local_fifo_rd_count[i] = 0;
	end
	 
	 for(i=0; i<TOTAL_FIFO_GROUPS; i++)
	   begin 
	      
	      for(j=0; j<4; j++)
		begin
		   assign fifo_rd_count_4[i][j] = local_fifo_rd_count[i*4 + j];
		   
		end
	      sort_4_fifos_by_rd_count 
		#(.FIFO_DEPTH_BITS(FIFO_DEPTH_BITS),
		  .TOTAL_CLUSTERS(4)
		  )
	      sort_fifo_by_rd_count_inst(
					 .clk(clk),
					 .rst_n(rst_n),
					 .srst_n(srst_n),
					 .fifo_rd_count(fifo_rd_count_4[i]), //fifo_rd_count[i+:3]),
					 .fifo_groups(fifo_groups[i])
					 );
	   end // for (i=0; i<TOTAL_FIFO_GROUPS; i++)
      end // block: sort_fifo_by_rd_count_gen
      
   endgenerate
   
endmodule // sort_fifo_by_rd_count


module sort_4_fifos_by_rd_count #(parameter FIFO_DEPTH_BITS = 6,
			       parameter TOTAL_CLUSTERS    = 4
			       )
   (
    input logic 		      clk,
    input logic 		      rst_n,
    input logic 		      srst_n,
    input logic [FIFO_DEPTH_BITS : 0] fifo_rd_count[TOTAL_CLUSTERS],
    output logic [TOTAL_CLUSTERS-1:0] fifo_groups[5]  
    );
/*
 Group 0 -> <8
 Group 1 -> 8 to 15
 Group 2 -> 16 to 31
 Group 3 -> 32 to 47
 Group 4 -> >47
 */
   generate
      begin : sort_4_fifos_by_rd_count_gen1
	 for(genvar z=0;z<TOTAL_CLUSTERS;z++)
	   always @ (posedge clk)
	     begin 
		if((!rst_n) | (!srst_n) )
		  begin
		     fifo_groups[0] = 4'hf;
		     for(int i= 1; i < 5; i++)
		       fifo_groups[i] = 0;
		  end
		else
		  begin
		     fifo_groups[0][z]   <= ((fifo_rd_count[z] >> 3) == 0);
		     fifo_groups[1][z]   <= ((fifo_rd_count[z] >> 3) == 1);
		     fifo_groups[2][z]   <= ((fifo_rd_count[z] >> 4) == 1);		  
		     fifo_groups[3][z]   <= ((fifo_rd_count[z] >> 4) == 2); 
		     fifo_groups[4][z]   <= ((fifo_rd_count[z] >> 4) == 3) ;		  
		  end
	     end // always @ (posedge b2b_clk)
      end // block: sort_4_fifos_by_rd_count_gen1
      
   endgenerate
   
endmodule // sort_fifo_by_rd_count


module find_max_4_fifos(
			input logic [3:0]  evt_available,
			input logic [3:0]  fifo_group_rd_idx[5],
			output logic [2:0] fifo_idx		
		     );
      genvar 				i, j;
   logic [2:0] 				local_fifo_idx[5]; //Based on number of groups 
  
   
  
   generate
      begin : find_max_4_fifos_gen
	 for(i=0; i < 5; i++)
	   begin 
	      max_fifo_by_flag max_fifo_by_flag_inst(evt_available, fifo_group_rd_idx[i], local_fifo_idx[i]);
	   end
	 
	 always_comb
	   begin
	      if(local_fifo_idx[4] != 4)
		begin
		   fifo_idx         = local_fifo_idx[4];	
		end
	      else if(local_fifo_idx[3] != 4)
		begin
		   fifo_idx         = local_fifo_idx[3];	
		end
	      else if(local_fifo_idx[2] != 4)
		begin
		   fifo_idx         = local_fifo_idx[2];	
		end
	      else if(local_fifo_idx[1] != 4)
		begin
		   fifo_idx         = local_fifo_idx[1];
		end
	      else 
		begin
		   fifo_idx         = local_fifo_idx[0]; //4; // <8 , wait for more data local_fifo_idx[0];	
		end	  
	   end // always_comb
      end // block: find_max_4_fifos_gen
      
   endgenerate
   
	    
endmodule // find_max_4_fifos


module get_fifo_idx_1st_stage (input logic [2:0] fifo_group_idx[5], output logic [2:0] fifo_idx);
     always_comb
	begin
	   if(fifo_group_idx[4] != 4)
	     begin
		fifo_idx         = fifo_group_idx[4];	
	     end
	   else if(fifo_group_idx[3] != 4)
	     begin
		fifo_idx         = fifo_group_idx[3];	
	     end
	   else if(fifo_group_idx[2] != 4)
	     begin
		fifo_idx         = fifo_group_idx[2];	
	     end
	   else if(fifo_group_idx[1] != 4)
	     begin
		fifo_idx         = fifo_group_idx[1];
	     end
	   else 
	     begin
		fifo_idx         = fifo_group_idx[0]; 
	     end	  
	end
endmodule // get_fifo_idx_1st_stage




module get_fifo_idx_2nd_stage #(
				parameter TOTAL_CLUSTERS=32
				)
   (
    input logic [5:0]  fifo_group_idx[5], 
    output logic [5:0] fifo_idx
    );
     always_comb
	begin
	   if(fifo_group_idx[4] != TOTAL_CLUSTERS)
	     begin
		fifo_idx         = fifo_group_idx[4];	
	     end
	   else if(fifo_group_idx[3] != TOTAL_CLUSTERS)
	     begin
		fifo_idx         = fifo_group_idx[3];	
	     end
	   else if(fifo_group_idx[2] != TOTAL_CLUSTERS)
	     begin
		fifo_idx         = fifo_group_idx[2];	
	     end
	   else if(fifo_group_idx[1] != TOTAL_CLUSTERS)
	     begin
		fifo_idx         = fifo_group_idx[1];
	     end
	   else 
	     begin
		fifo_idx         = fifo_group_idx[0]; 
	     end	  
	end
endmodule


module sort_4_fifos(
			input logic [3:0]  evt_available,
			input logic [3:0]  fifo_group_rd_idx[5],
			output logic [2:0] fifo_idx[5] //Based on number of groups
		     );
      genvar 				i, j;
  
  
   
  
   generate 
      begin: sort_4_fifos_gen
	 for(i=0; i < 5; i++)
	   begin : max_fifo_by_flag
	      max_fifo_by_flag max_fifo_by_flag_inst(evt_available, fifo_group_rd_idx[i], fifo_idx[i]);
	   end
      end
   endgenerate
endmodule 


module consolidate_4_groups #(
			    parameter TOTAL_CLUSTERS=32,
			    parameter MAX_CLUSTERS_BLEN = 5
			    )
   (input logic [2:0] fifo_group[4][5], input logic [MAX_CLUSTERS_BLEN:0] offset, output logic [MAX_CLUSTERS_BLEN:0]  fifo_group_idx[5]);
   always_comb
     begin
	for(int i=0; i < 5; i++)
	  begin
	     if(fifo_group[0][i] != 4)
	       begin
		  fifo_group_idx[i] = fifo_group[0][i];
	       end
	     else if(fifo_group[1][i] != 4)
	       begin
		  fifo_group_idx[i] = fifo_group[1][i] + offset;
	       end
	     else if(fifo_group[2][i] != 4)
	       begin
	     fifo_group_idx[i] = fifo_group[2][i] + (offset << 1);
	       end
	     else if(fifo_group[3][i] != 4)
	       begin
		  fifo_group_idx[i] = fifo_group[2][i] + (offset << 2);
	       end
	     else
	       begin
		  fifo_group_idx[i] = TOTAL_CLUSTERS;	     
	       end	
	  end // for (int i=0; i < 5; i++)
     end
endmodule // consolidate_4_groups



module consolidate_2_groups #(
			    parameter TOTAL_CLUSTERS=32,
			    parameter MAX_CLUSTERS_BLEN = 5
			    )
   (input logic [2:0] fifo_group[2][5], input logic [MAX_CLUSTERS_BLEN:0] offset, output logic [MAX_CLUSTERS_BLEN:0]  fifo_group_idx[5]);
   always_comb
     begin
	for(int i=0; i < 5; i++)
	  begin
	     if(fifo_group[0][i] != 4)
	       begin
		  fifo_group_idx[i] = fifo_group[0][i];
	       end
	     else if(fifo_group[1][i] != 4)
	       begin
		  fifo_group_idx[i] = fifo_group[1][i] + offset;
	       end
	     else
	       begin
		  fifo_group_idx[i] = TOTAL_CLUSTERS;	     
	       end	
	  end // for (int i=0; i < 5; i++)
     end
endmodule // consolidate_2_groups


module consolidate_groups_offsets #(
			    parameter TOTAL_CLUSTERS=32
			    )
   (input logic fifo_group[4], input logic offset, output logic [5:0]  fifo_group_idx);
   always_comb
     begin
	if(fifo_group[0] != TOTAL_CLUSTERS)
	  begin
	     fifo_group_idx = fifo_group[0];
	  end
	else if(fifo_group[1] != TOTAL_CLUSTERS)
	  begin
	     fifo_group_idx = fifo_group[1] + offset;
	  end
	else if(fifo_group[2] != TOTAL_CLUSTERS)
	  begin
	     fifo_group_idx = fifo_group[2] + (offset << 1);
	  end
	else if(fifo_group[3] != TOTAL_CLUSTERS)
	  begin
	     fifo_group_idx = fifo_group[2] + (offset << 2);
	  end
	else
	  begin
	     fifo_group_idx = TOTAL_CLUSTERS;	     
	  end	
     end
endmodule

module find_max_fifo
  #(
    parameter TOTAL_CLUSTERS=4,
    parameter TOTAL_CLUSTER_GROUPS = 1,
    parameter OUT_BIT_LEN = 2
    )
   (
    input logic [TOTAL_CLUSTERS-1:0] evt_available,
    input logic [3:0] 		     fifo_groups[TOTAL_CLUSTER_GROUPS][5],
    output logic [OUT_BIT_LEN:0]     fifo_idx
    );
   parameter SECOND_STAGE_GROUPS = TOTAL_CLUSTER_GROUPS/4 + (TOTAL_CLUSTER_GROUPS&3 != 0); //$ceil(TOTAL_CLUSTER_GROUPS/4);
   parameter THIRD_STAGE_GROUPS  = SECOND_STAGE_GROUPS/4 + (SECOND_STAGE_GROUPS&3 != 0); //$ceil(SECOND_STAGE_GROUPS/4);
   parameter MAX_CLUSTERS        = 32;
   parameter MAX_CLUSTERS_BLEN   = $clog2(32);
      
   genvar 			     i, j, k;
   logic [2:0] 			     grp_fifo_idx[TOTAL_CLUSTER_GROUPS][5]; //Based on number of groups
   logic [2:0] 			     grp_fifo_idx_2nd[SECOND_STAGE_GROUPS][4][5]; //Based on number of groups 
      
   logic [OUT_BIT_LEN:0] 	     first_stage_fifo_idx;
   logic [OUT_BIT_LEN:0] 	     second_stage_fifo_idx;
   logic [2:0] 			     grp_fifo_idx_transpose[5][TOTAL_CLUSTER_GROUPS];
   logic [MAX_CLUSTERS_BLEN:0] 	     second_stage_grp[SECOND_STAGE_GROUPS][5];
   logic [MAX_CLUSTERS_BLEN:0] 	     third_stage_grp[5];
   
   
   
   if(SECOND_STAGE_GROUPS == 1)
     assign fifo_idx = first_stage_fifo_idx;
   else if(THIRD_STAGE_GROUPS == 1)
     assign fifo_idx = second_stage_fifo_idx;
   else
     assign fifo_idx = TOTAL_CLUSTERS;
   
   generate
      begin  : find_max_fifo_gen
	 for(i=0; i < TOTAL_CLUSTER_GROUPS; i++)
	   begin : sort_4_fifos_inst
	      
	      sort_4_fifos sort_4_fifos_inst(
					     .evt_available(evt_available[i+:4] ),
					     .fifo_group_rd_idx(fifo_groups[i]),
					     .fifo_idx(grp_fifo_idx[i])
					     
					     );
	      
	   end
	 //if second stage groups > 1
	 //Split local_fifo_data_range in groups of 4
	 //      {
	 //if third stage groups > 1
	 //}
	 //else{
	 //find max
	 //}
	 
	 if(SECOND_STAGE_GROUPS == 1)
	   begin : first_stage
	      get_fifo_idx_1st_stage get_fifo_idx_1st_stage_inst(grp_fifo_idx[0], first_stage_fifo_idx);	   
	   end
	 else
	   begin : second_stage
	    /*  for(i=0; i < TOTAL_CLUSTER_GROUPS; i++)
		begin
		   for(j=0; j<5; j++)
		     begin
			assign grp_fifo_idx_transpose[j][i] = grp_fifo_idx[i][j];
		     end
		end
	     */
	      for(i=0; i < SECOND_STAGE_GROUPS; i++)
		begin
		   for(j=0; j<4; j++)
		     begin
			for(k=0;k<5;k++)
			  begin
			     if(i*4 + j == TOTAL_CLUSTER_GROUPS)
			       assign grp_fifo_idx_2nd[i][j][k] = 4;
			     else
			       assign grp_fifo_idx_2nd[i][j][k]= grp_fifo_idx[i*4 + j][k];
			  end
		     end
		end
	      
	      for(j=0; j < SECOND_STAGE_GROUPS; j++)
		begin
		   consolidate_4_groups
		    #(
		      .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
		      .MAX_CLUSTERS_BLEN(MAX_CLUSTERS_BLEN)
		      )
		   pick_2nd_stage_idx_inst(
					   grp_fifo_idx_2nd[j], //grp_fifo_idx_transpose[i+:4], 
					   4 , 
					   second_stage_grp[j]
					   );
		   
		end // for (j=0; j < SECOND_STAGE_GROUPS; j++)
	      
	      if(THIRD_STAGE_GROUPS == 1)
		begin: third_stage_results
		   get_fifo_idx_2nd_stage #(
					    .TOTAL_CLUSTERS(TOTAL_CLUSTERS)
					    )
		   get_fifo_idx_2nd_stage_inst (
						.fifo_group_idx(third_stage_grp),
						.fifo_idx(second_stage_fifo_idx)
						);
		   
		   consolidate_2_groups
		     #(
		       .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
		       .MAX_CLUSTERS_BLEN(MAX_CLUSTERS_BLEN)
		       )
		   pick_3rd_stage_idx_inst(
					   second_stage_grp, //grp_fifo_idx_transpose[i+:4], 
					   16 , 
					   third_stage_grp
					   );
		end
	      else
		begin
		   //Not supported
		   
		end
	   end // else: !if(SECOND_STAGE_GROUPS == 1)
      end // block: find_max_fifo_gen
      
   endgenerate
endmodule // find_max_fifo

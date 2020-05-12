module cluster_sync_engine #(
			     parameter DATA_WIDTH = 65,
			     parameter EVT_HDR_BITS=40,
			     parameter TOTAL_CLUSTERS=4,
			     parameter FIFO_DEPTH_BITS=9
			     )
  (
   input logic 			    clk,
   input logic 			    rst_n,
   input logic 			    srst_n,
   
   input logic [EVT_HDR_BITS-1:0]   evt_l0id[TOTAL_CLUSTERS],
   input logic [1:0] 		    evt_available[TOTAL_CLUSTERS],
   input logic [FIFO_DEPTH_BITS:0]  cre_fifo_rd_data_count[TOTAL_CLUSTERS],
//   input logic [TOTAL_CLUSTERS-1:0] cre_fifo_almost_full,
//   input logic [TOTAL_CLUSTERS-1:0] cre_fifo_half_full,
   output logic [1:0] 		    evt_ctrl[TOTAL_CLUSTERS],
   output logic [2:0] 		    cluster_sel	    
   );
   parameter  WAIT = 0;
   parameter  TX   = 1;
   parameter  DROP = 2;

   parameter  OUT_BIT_LEN       = $clog2(TOTAL_CLUSTERS);
   parameter  TOTAL_FIFO_GROUPS = $ceil(TOTAL_CLUSTERS/4);
   
   
   
   logic [1:0] 		      next_evt_ctrl;
   logic [EVT_HDR_BITS-1:0]   cur_l0id;
   logic [EVT_HDR_BITS-1:0]   prev_l0id;
   logic [TOTAL_CLUSTERS-1:0] active_cluster;
   logic [OUT_BIT_LEN:0]      total_evt_hdr;
   logic [TOTAL_CLUSTERS-1:0] active_ftr;
   logic 		      first_ehdr;
   logic [OUT_BIT_LEN:0]      evt_hdr_tx_idx;
   logic [3:0] 		      evt_hdr_tx_flag;
   
   
   logic [1:0] 		      evt_hdr_ctrl_internal[TOTAL_CLUSTERS+1];
   logic [1:0] 		      evt_m_ctrl_internal[TOTAL_CLUSTERS+1];
   logic [1:0] 		      evt_ftr_ctrl_internal[TOTAL_CLUSTERS+1];
   logic 		      m_locked;

   logic [TOTAL_CLUSTERS-1:0] evt_hdr_available;
   logic [TOTAL_CLUSTERS-1:0] evt_m_available;
   logic [TOTAL_CLUSTERS-1:0] evt_ftr_available;

   logic [TOTAL_CLUSTERS-1:0] evt_ftr_available_d[2];
   logic [TOTAL_CLUSTERS-1:0] evt_m_available_d[3];
   				    
   logic [OUT_BIT_LEN:0] m_tx_idx;
   logic [OUT_BIT_LEN:0] ftr_tx_idx;
   logic [TOTAL_CLUSTERS-1 :0] evt_ftr_cnt;
   logic [TOTAL_CLUSTERS-1 :0] evt_ftr_rx;

 
   localparam E_NOT_AV = 0;
   localparam EHDR_AV  = 1;
   localparam M_AV     = 2;
   localparam EFTR_AV  = 3;

   
 
   logic [OUT_BIT_LEN:0]       ehdr_fifo_idx;
   logic [OUT_BIT_LEN:0]       m_fifo_idx;
   logic [OUT_BIT_LEN:0]       eftr_fifo_idx;

   logic [OUT_BIT_LEN:0]       ehdr_fifo_idx_i;
   logic [OUT_BIT_LEN:0]       m_fifo_idx_i[2];
   logic [OUT_BIT_LEN:0]       eftr_fifo_idx_i[2];

   logic [OUT_BIT_LEN:0]       fifo_max_inter[TOTAL_CLUSTERS/2];
   logic [OUT_BIT_LEN:0]       fifo_max_inter_i[TOTAL_CLUSTERS/2];
   logic [OUT_BIT_LEN:0]       fifo_min_inter[TOTAL_CLUSTERS/2];
   logic [OUT_BIT_LEN:0]       fifo_mid_inter[TOTAL_CLUSTERS/2];
   logic [OUT_BIT_LEN:0]       fifo_max_order[TOTAL_CLUSTERS];
   
   logic [TOTAL_CLUSTERS-1:0]  fifo_groups[TOTAL_FIFO_GROUPS][5];
   logic [TOTAL_CLUSTERS-1:0]  fifo_groups_4[5];
   
/*   sort_4_fifos_by_rd_count 
     #(.FIFO_DEPTH_BITS(FIFO_DEPTH_BITS),
       .TOTAL_CLUSTERS(TOTAL_CLUSTERS)
       )
   sort_fifo_by_rd_count_inst(
			      .clk(clk),
			      .rst_n(rst_n),
			      .srst_n(srst_n),
			      .fifo_rd_count(cre_fifo_rd_data_count),
			      .fifo_groups(fifo_groups_4)
			      );
   
   find_max_4_fifos ehdr_find_max_fifo_inst(evt_hdr_available,fifo_groups_4,ehdr_fifo_idx_i);
   find_max_4_fifos m_find_max_fifo(evt_m_available,fifo_groups_4,m_fifo_idx);
   find_max_4_fifos eftr_find_max_fifo(evt_ftr_available,fifo_groups_4,eftr_fifo_idx);
   */
   
   sort_fifo_by_rd_count #(
			   .FIFO_DEPTH_BITS(FIFO_DEPTH_BITS),
			   .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
			   .TOTAL_FIFO_GROUPS(TOTAL_FIFO_GROUPS)
			   )
   sort_fifo_by_rd_count(
			 .clk(clk),
			 .rst_n(rst_n),
			 .srst_n(srst_n),
			 .fifo_rd_count(cre_fifo_rd_data_count),
			 .fifo_groups(fifo_groups)
			 );
			 
   find_max_fifo  #(
		    .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
		    .TOTAL_CLUSTER_GROUPS(TOTAL_FIFO_GROUPS),
		    .OUT_BIT_LEN(OUT_BIT_LEN)
		    )
   ehdr_find_max_fifo (
		       .evt_available(evt_hdr_available), 
		       .fifo_groups(fifo_groups),
		       .fifo_idx(ehdr_fifo_idx)
		       );


   find_max_fifo  #(
		    .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
		    .TOTAL_CLUSTER_GROUPS(TOTAL_FIFO_GROUPS),
		    .OUT_BIT_LEN(OUT_BIT_LEN)
		    )
   m_find_max_fifo (
		       .evt_available(evt_m_available), 
		       .fifo_groups(fifo_groups),
		       .fifo_idx(m_fifo_idx)
		       );

   find_max_fifo  #(
		    .TOTAL_CLUSTERS(TOTAL_CLUSTERS),
		    .TOTAL_CLUSTER_GROUPS(TOTAL_FIFO_GROUPS),
		    .OUT_BIT_LEN(OUT_BIT_LEN)
		    )
   eftr_find_max_fifo (
		       .evt_available(evt_ftr_available), 
		       .fifo_groups(fifo_groups),
		       .fifo_idx(eftr_fifo_idx)
		       );
   
     always_comb 
     begin
	for(int i=0; i< TOTAL_CLUSTERS/2; i++)
	  begin
	     if(cre_fifo_rd_data_count[i] > cre_fifo_rd_data_count[i+TOTAL_CLUSTERS/2])
	       begin
		  fifo_max_inter[i] = i;
	       end
	     else
	       begin
		  fifo_max_inter[i] = i + TOTAL_CLUSTERS/2;
	       end


	     if(cre_fifo_rd_data_count[i] <= cre_fifo_rd_data_count[i+TOTAL_CLUSTERS/2])
	       begin
		  fifo_min_inter[i] = i;
	       end
	     else
	       begin
		  fifo_min_inter[i] = i + TOTAL_CLUSTERS/2;
	       end
	  end // for (int i=0; i< TOTAL_CLUSTERS/2; i++)



     end // always_comb

     always @ (posedge clk)
     begin
	if(~rst_n || ~srst_n)
	  begin
	     for(int i=0; i< TOTAL_CLUSTERS; i++)
	       fifo_max_order[i] <= TOTAL_CLUSTERS;
	    

	     for(int i=0; i< TOTAL_CLUSTERS/2; i++)
	       begin
		  fifo_mid_inter[i]   <= TOTAL_CLUSTERS;
		  fifo_max_inter_i[i] <= TOTAL_CLUSTERS;
	       end
	     
	  end
	else
	  begin
	     if(cre_fifo_rd_data_count[fifo_max_inter[0]] > cre_fifo_rd_data_count[fifo_max_inter[1]])
	       begin
		  fifo_max_inter_i[0] <= fifo_max_inter[0];
		  fifo_mid_inter[0]   <= fifo_max_inter[1];
		  
	       end
	     else
	       begin
		  fifo_max_inter_i[0] <= fifo_max_inter[1];
		  fifo_mid_inter[0]   <= fifo_max_inter[0];
	       end


	     if(cre_fifo_rd_data_count[fifo_min_inter[0]] < cre_fifo_rd_data_count[fifo_min_inter[1]])
	       begin
		  fifo_max_inter_i[1] <= fifo_min_inter[0];
		  fifo_mid_inter[1]   <= fifo_min_inter[1];
	       end
	     else
	       begin
		  fifo_max_inter_i[1] <= fifo_min_inter[1];
		  fifo_mid_inter[1]   <= fifo_min_inter[0];
	       end

	     fifo_max_order[0] <= fifo_max_inter_i[0];
	     fifo_max_order[3] <= fifo_max_inter_i[1];
	     	     
	     if(cre_fifo_rd_data_count[fifo_mid_inter[0]] > cre_fifo_rd_data_count[fifo_mid_inter[1]])
	       begin
		  fifo_max_order[1] <= fifo_mid_inter[0];
		  fifo_max_order[2] <= fifo_mid_inter[1];
	       end
	     else
	       begin
		  fifo_max_order[1] <= fifo_mid_inter[1];
		  fifo_max_order[2] <= fifo_mid_inter[0];
	       end
	  end // else: !if(~rst_n || ~srst_n)
     end // always @ (posedge clk)

   /*
   always_comb
     begin
	if(evt_hdr_available[fifo_max_order[0]])
	  ehdr_fifo_idx = fifo_max_order[0];
	else if(evt_hdr_available[fifo_max_order[1]])
	  ehdr_fifo_idx = fifo_max_order[1];
	else if(evt_hdr_available[fifo_max_order[2]])
	  ehdr_fifo_idx = fifo_max_order[2];
	else if(evt_hdr_available[fifo_max_order[3]])
	  ehdr_fifo_idx = fifo_max_order[3];
	else
	  ehdr_fifo_idx = TOTAL_CLUSTERS;
	
     end // always_comb

    always_comb
     begin
	if(evt_m_available[fifo_max_order[0]])
	  m_fifo_idx = fifo_max_order[0];
	else if(evt_m_available[fifo_max_order[1]])
	  m_fifo_idx = fifo_max_order[1];
	else if(evt_m_available[fifo_max_order[2]])
	  m_fifo_idx = fifo_max_order[2];
	else if(evt_m_available[fifo_max_order[3]])
	  m_fifo_idx = fifo_max_order[3];
	else
	  m_fifo_idx = TOTAL_CLUSTERS;
	
     end // always_comb

     always_comb
     begin
	if(evt_ftr_available[fifo_max_order[0]] &  evt_ftr_ctrl_internal[fifo_max_order[0]] != DROP)
	  eftr_fifo_idx = fifo_max_order[0];
	else if(evt_ftr_available[fifo_max_order[1]] &  evt_ftr_ctrl_internal[fifo_max_order[1]] != DROP)
	  eftr_fifo_idx = fifo_max_order[1];
	else if(evt_ftr_available[fifo_max_order[2]] &  evt_ftr_ctrl_internal[fifo_max_order[2]] != DROP)
	  eftr_fifo_idx = fifo_max_order[2];
	else if(evt_ftr_available[fifo_max_order[3]] &  evt_ftr_ctrl_internal[fifo_max_order[3]] != DROP)
	  eftr_fifo_idx = fifo_max_order[3];
	else
	  eftr_fifo_idx = TOTAL_CLUSTERS;
	
     end
   
  
   always_comb
     begin
	if(ehdr_fifo_idx_i[0] != TOTAL_CLUSTERS)
	  begin
	     ehdr_fifo_idx  <= ehdr_fifo_idx_i[0];
	  end
	else if(ehdr_fifo_idx_i[1] != TOTAL_CLUSTERS)
	  begin
	     ehdr_fifo_idx  <= ehdr_fifo_idx_i[1];
	  end
	else if(ehdr_fifo_idx_i[2] != TOTAL_CLUSTERS)
	  begin
	     ehdr_fifo_idx  <= ehdr_fifo_idx_i[2];
	  end
	else
	  begin
	     ehdr_fifo_idx  <= TOTAL_CLUSTERS;
	  end
     end // always_comb
   */
   
   
   
   genvar      i;
   generate
      begin
	 for(i=0;i<TOTAL_CLUSTERS;i++)
	   begin
	      assign evt_ctrl[i] = (evt_hdr_available[i])? (evt_hdr_ctrl_internal[i]) : 
				   (
				    (evt_m_available[i])?evt_m_ctrl_internal[i] :
				    ((evt_ftr_available[i])? evt_ftr_ctrl_internal[i] : 0)
				    );
	      
	      assign evt_hdr_available[i] = (evt_available[i]==EHDR_AV);
	      assign evt_m_available[i]   = (evt_available[i]==M_AV);
	      assign evt_ftr_available[i] = (evt_available[i]==EFTR_AV);
	   end
      end 


      
   endgenerate;
  
  

   always_comb
     begin
	if(evt_hdr_ctrl_internal[evt_hdr_tx_idx] == TX)
	  begin
	     cluster_sel <= evt_hdr_tx_idx;
	  end 
	else if(m_locked)
	  begin
	     cluster_sel <= m_tx_idx;
	  end
	else if(evt_ftr_available[ftr_tx_idx]==TX)
	  begin
	     cluster_sel <= ftr_tx_idx;
	  end
	else
	  begin
	     cluster_sel <= TOTAL_CLUSTERS; //invalid value
	  end
	//	  end // else: !if(~rst_n || ~srst_n)
     end // always_comb
   
   
   
   always @ (posedge clk)
     begin
	if(~rst_n || ~srst_n)
	  begin
	     cur_l0id       <= 0;
	     prev_l0id      <= 0;
	     active_cluster <= 0;
	     first_ehdr     <= 0;
	     evt_hdr_tx_idx <= TOTAL_CLUSTERS;
	     evt_hdr_tx_flag <= 0;
	 
	     
	     for(int i=0;i <4; i++)
	       begin
		  evt_hdr_ctrl_internal[i] <= WAIT;
	       end
	  end
	else
	  begin	  
	     
	     if(cur_l0id == 0)
	       begin
		  if(evt_hdr_available)
		    begin
		       if(first_ehdr == 0)
			 begin
			    first_ehdr         <= 1'b1;
			    for(int i=0; i< TOTAL_CLUSTERS; i++)
			      begin
				 if(i==ehdr_fifo_idx)
				   begin
				      evt_hdr_ctrl_internal[i] <= TX;
				      cur_l0id                 <= evt_l0id[i];
				      evt_hdr_tx_idx           <= i;
				      evt_hdr_tx_flag[i]       <= 1;
				   end
				 else
				   begin
				      evt_hdr_ctrl_internal[i] <= WAIT;
				   end
			      end
			 end
		    end
	       end // if (cur_l0id == 0)
	     else
	       begin
		  if(evt_ftr_cnt == TOTAL_CLUSTERS  && evt_ftr_available == 0)
		    begin
		       prev_l0id       <= cur_l0id;
		       cur_l0id        <= 0;
		       first_ehdr      <= 0;
		    end
		  
		  for(int i=0; i<TOTAL_CLUSTERS; i++)
		    begin
		       if(evt_hdr_available[i] & evt_hdr_tx_idx != i)
			 begin
			    if(cur_l0id == evt_l0id[i])
			      begin
				 evt_hdr_ctrl_internal[i] <= DROP;
				 evt_hdr_tx_flag[i]       <= 1;
			      end
			   	 end
		       else if(evt_hdr_available[i]==0  & evt_hdr_tx_idx == i)
			 begin
			    evt_hdr_ctrl_internal[i] <= WAIT;
			    evt_hdr_tx_idx           <= TOTAL_CLUSTERS;
//			    $display("$time evt_hdr_available[%d]=%d, evt_hdr_tx_idx=%d", i, evt_hdr_available[i],evt_hdr_tx_idx);
			    
			 end
		       else if(~evt_hdr_available[i])
			  evt_hdr_ctrl_internal[i] <= WAIT;
		       
		      
			 
		    end // for (int i=0; i<TOTAL_CLUSTERS; i++)
		  
	       end // else: !if(cur_l0id == 0)
	  end
     end // always @ (posedge clk)
   

//evt_m_ctrl_internal
    
   always @ (posedge clk)
     begin
	if(~rst_n || ~srst_n)
	  begin
	     m_locked     <= 0;
	     m_tx_idx     <= TOTAL_CLUSTERS+1;
	     for(int i=0;i <3; i++)
	       begin
		  evt_m_available_d[i] = 0;
	       end
	     
	     for(int i=0;i <4; i++)
	       begin
		  evt_m_ctrl_internal[i] <= WAIT;
		 
	       end
	  end
	else
	  begin
	     evt_m_available_d[0] <= evt_m_available;
	     evt_m_available_d[1] <= evt_m_available_d[0];
	     evt_m_available_d[2] <= evt_m_available_d[1];
	     
	     if(cur_l0id != 0 && m_locked == 0)
	       begin
	//	  if(evt_m_available_d[2][m_fifo_idx])
		  if(evt_m_available[m_fifo_idx])
		    begin
		       for(int i=0; i<TOTAL_CLUSTERS; i++)
			 begin
			    m_locked <= 1;
			    if(i == m_fifo_idx)
			      begin
				 evt_m_ctrl_internal[i] <= TX;
				 m_tx_idx               <= i;
			      end
			    else
			      begin
				 evt_m_ctrl_internal[i] <= WAIT;
			      end
			 end // for (int i=0; i<TOTAL_CLUSTERS; i++)
		    end // if (evt_m_available[m_fifo_idx])
		  else
		    begin
		       m_locked  <= 0;
		       m_tx_idx  <= TOTAL_CLUSTERS+1;
		       
		       for(int i=0; i<TOTAL_CLUSTERS; i++)
			 begin
			    evt_m_ctrl_internal[i] <= WAIT;
			 end
		    end
	       end // if (cur_l0id != 0 && m_locked == 0)
	     else
	       begin
		  if(m_locked == 1 && evt_m_available[m_tx_idx] == 0) //Module should be flagged as available even if stalled due to FIFO full
		    begin
		       m_locked <= 0;
		       evt_m_ctrl_internal[m_tx_idx] <= WAIT;
		       m_tx_idx                      <= TOTAL_CLUSTERS+1;
		    end
	       end // else: !if(cur_l0id == 0)
	  end
     end // always @ (posedge clk)
   


   //Event Footer
    always @ (posedge clk)
     begin
	if(~rst_n || ~srst_n)
	  begin
	     ftr_tx_idx <= TOTAL_CLUSTERS;
	     
	     evt_ftr_rx  <= 0;
	     evt_ftr_cnt <= 0;
	     for(int i=0; i<2; i++)
	       begin
		  evt_ftr_available_d[i] <= 0;
	       end
	     
	     for(int i=0;i < TOTAL_CLUSTERS+1; i++)
	       begin
		  evt_ftr_ctrl_internal[i] <= WAIT;
		  
	       end
	  end
	else
	  begin
	     
	     evt_ftr_available_d[0] <= evt_ftr_available;
	     evt_ftr_available_d[1] <= evt_ftr_available_d[0];
	     
	     if(cur_l0id != 0)
	       begin
		  if(evt_ftr_available)
		    begin
		       for(int i=0; i< TOTAL_CLUSTERS; i++)
			 begin
			    if(i == eftr_fifo_idx && evt_ftr_available[i])
			      begin
				 if(evt_ftr_rx[i] == 0)
				   begin
				      evt_ftr_rx[i]             <= 1;
				      evt_ftr_cnt               <= evt_ftr_cnt +1;
				      if(evt_ftr_cnt == TOTAL_CLUSTERS - 1)
					begin
					   evt_ftr_ctrl_internal[i] <= TX;
					   ftr_tx_idx               <= i;
					end     
				      else
					begin
					  
					   evt_ftr_ctrl_internal[i] <= DROP;
					end
				   end // if (evt_ftr_rx[i] == 0)
			      end // if (i == eftr_fifo_idx)
			    else
			      begin
				 if(evt_ftr_available[i] == 0)
				   begin
				      evt_ftr_ctrl_internal[i] <= WAIT;
				   end
			      end // else: !if(i == eftr_fifo_idx)
			    
			 end // for (int i=0; i< TOTAL_CLUSTERS; i++)
		       
		    end // if (evt_ftr_available)
		  else
		    begin
		       for(int i=0; i < TOTAL_CLUSTERS; i++)
			 begin
			    if(evt_ftr_available[i] == 0)
			      begin
				 evt_ftr_ctrl_internal[i] <= WAIT;
			      end
			 end
		    end
		  
	       end // if (cur_l0id != 0)
	     
	     else
	       begin
		  evt_ftr_cnt <= 0;
		  ftr_tx_idx <= TOTAL_CLUSTERS;
		  evt_ftr_rx  <= 0;
		  
		  for(int i=0; i < TOTAL_CLUSTERS; i++)
		    evt_ftr_ctrl_internal[i] <= WAIT;
		  
	       end // else: !if(cur_l0id == 0)
	  end
     end // always @ (posedge clk)
   


   
   
   
endmodule // cluster_sync_engine

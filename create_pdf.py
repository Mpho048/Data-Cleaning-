import fpdf 
import pandas as pd
import os
import pandas as pd 
from pypdf import PdfReader,PdfWriter 
import sqlite3 as sql
import pdfplumber as plb
from datetime import datetime


#================================
# GENERATE PDF
#================================
class PDF(fpdf.FPDF):
    def __init__(self,bg_color=(26,54,93),header_text = "Data Analysis Report"):
        super().__init__()
        self.bg_color = bg_color
        self.header_text = header_text

        
    def header(self):
        self.set_fill_color(*self.bg_color) 
        self.rect(0, 0, 210, 4, 'F')
        
        self.set_font("helvetica", "B", 12)
        self.set_text_color(26, 54, 93) 
        self.cell(0, 10,self.header_text, 0, 1)
        self.set_draw_color(226, 232, 240)
        self.line(self.l_margin, 13, self.w - self.r_margin, 13)
        self.ln(4)         
         
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")
                
#================================
#Internal Helpers
#================================

    def _divider(self):
        y = self.get_y()
        self.set_draw_color(180,180,180)
        self.line(self.l_margin, y,self.w - self.r_margin,y)
        self.ln(5)
        
    def _check_page(self,required_space=40):
        mark = self.h-self.b_margin-required_space
        
        if (self.get_y() > mark):
            self.add_page()                                               

    def  _clean_text(self,value):
        
        if value is None:
            return "" 
        return str(value).replace("\n"," ")

    def _metric_row(self,data):
        total = len(data)
        spacing  = 5
        width = (self.epw -(spacing*(total-1)))/ total
        height = 20
        start_y = self.get_y()
        
        for title,val in data:
            x = self.get_x()
            
            self.set_fill_color(245,245,245)
            self.rect(x,start_y,width,height,"F") 
            self.set_xy(x,start_y +3)
            
            self.set_font("helvetica","",10)
            self.cell(width,6,str(title),align = "C")
            self.set_xy(x,start_y+11)
            
            self.set_font("helvetica","B",13)
            self.cell(width,6,str(val),align = "C")
            self.set_x(x+width+spacing)
        self.set_y(start_y + height +8)

    def _finding_box(self,text):
        self.set_fill_color(245,245,245)
        
        self.multi_cell(0,8,f"- {text}",border = 1,fill = True)
        self.ln(2) 
                                                            
    def _auto_col_width(self,df,min_width = 25):
        
        page_width = self.w - (2 * self.l_margin)
        return page_width /len(df.columns)
        
    def _format_size(self, df):
        # Convert total bytes straight to KB
        size_kb = df.memory_usage(deep=True).sum() / 1024
        
        # If it's less than 1024 KB, keep it as KB
        if size_kb < 1024:
            return f"{round(size_kb, 2)} KB"
        
        # Otherwise, convert to MB
        size_mb = size_kb / 1024
        return f"{round(size_mb, 2)} MB"
 

#===============================
#Title 
#===============================                
    def Set_title(self, title, font  = "helvetica", text_color=(255, 255, 255), no_color="N"):
        self.set_font(font, "B", 16)
        if no_color.upper() == "Y":
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(5)
        else:
            self.set_fill_color(*self.bg_color)
            self.set_text_color(*text_color)
            
            self.set_font("helvetica","B",16)
            self.cell(0,15,str(title),fill=True,ln = True, align = "C")
            self.set_text_color(0, 0, 0)
            self.ln(8)
        self.set_fill_color(255,255,255)
        
#==========================
#TEXT
#===========================
         
    def write_txt(self, word, align="L", multi=False):
        
        self.set_font("helvetica", "", 10)
        if multi:
            self.multi_cell(0, 6, word, align=align)
            self.ln(3)
        else:
            self.cell(0, 6, word, ln=True, align= align)
        
    def _get_cols(self, df, W,name=""):
        self.set_fill_color(*self.bg_color)
        #self.set_text_color(255,255,255)
        self.set_font("helvetica", style="B", size=10)
        for i, col in enumerate(df.columns):
            header_text = str(name) if (i == 0 and name) else str(col)
            self.set_text_color(255,255,255)
            self.cell(W,8,header_text,border=1,align="C",fill=True)
        self.set_text_color(0,0,0,)
        self.ln()

#===========================
#TABLES
#===========================        

    def single_col(self,df,col = "Cols"):
        """ For a serious
        use form Series to pdf
        data.name  = name
        Args:
            col:str = 'Cols'
            df: pd.Series()
        """
        if df.name == None:
            df.name = "Value"
        data = [(str(col),df.name)]+list(df.items())
        self.set_font("helvetica",size = 12)
        with self.table() as table:
            for index in data:
                row = table.row()
                for val in index:
                    row.cell(str(val))
        self.ln()       
                
    def create_table(self, df,H=8, size=9, font="helvetica", name=""):
        """Unified dynamic grid table engine"""
        width = self._auto_col_width(df)
        self.set_fill_color(26,54,93)
        self._get_cols(df,width,name)
        
        self.set_font("helvetica","",size)
        for _,rows in df.iterrows():
            
            self._check_page()            
            for row in rows:
                text = self._clean_text(row)
                text = text[:15]+"..." if len(text)>15 else text
                self.cell(width,8,text,border = 1)
            self.ln()
        self.ln(4)           

    def show_info(self, df, names=None, url="None"):
        data = df.copy()
        data.rename(columns=str.lower, inplace=True)       
        if isinstance(names, dict) and names:
            data.rename(columns=names, inplace=True)
            
        self.set_font("helvetica", "B", 11)
        page_width = self.w - 2 * self.l_margin
        col_width = page_width / len(data.columns)
        line_height = self.font_size * 2.5
        
        # Kept it clean and direct
        self.cell(0, 10, "1. Input Dataset Preview (First 5 Rows):", ln=True)
        self.ln(2)
        
        self._get_cols(data, W=col_width, H=line_height)
        self.set_font("helvetica", "", 9)        
        for _, row_series in data.head(5).iterrows():
            for val in row_series.values:
                cell_text = f"{val:.2f}" if isinstance(val, (float, int)) else str(val)
                self.cell(col_width, line_height, cell_text, border=1, ln=0, align="C")
            self.ln()
        
        self.ln(5) 
        self.set_font("helvetica", "B", 11)
        self.cell(0, 10, "2. Source Code & Repository:", ln=True)
        self.set_font("helvetica", "", 10)
        
        # TWEAKED TEXT: Matching your precise, conversational tone
        self.write(5, "Okey want to check the full python script and code layout? You can find the entire repository online.\n")
        
        self.set_text_color(0, 0, 255)
        self.set_font("helvetica", "U")
        self.write(5, f"Click here to see the Python script on GitHub:[{url}].", link=url)
        self.set_text_color(0, 0, 0)
        self.set_font("helvetica", "", 10)
        self.ln(10)

#========Analysis Pages==========

    def add_graph_page(self,img_path,title,summary,w = 140,h = 75):
        """ 
        Place a large centered graph layout,followed by an analytic summary  directly below
        Args
        img_path(str):
            Image path
        title(str):
            Title for the graph
        summary(str)
        w(int) = 140:
            width of the image
        h(int) = 75:
            height of the image       
        """
        #check spacing
        self._check_page(h + 10)
        current_y = self.get_y()
        
        #calc dynamic  horizontal centered coordinate
        new_width =  self.w - self.l_margin - self.r_margin
        centered_x = self.l_margin + (new_width - w) / 2
        
        if os.path.exists(img_path):
            self.image(img_path,x = centered_x,y = current_y,w = w,h = h)
            self.set_y(current_y + h + 4)
            
        self._check_page(25)
        
        #Header for summary
        self.set_font("helvetica","B",11) 
        self.set_text_color(26,54,93)
        self.cell(0,8,str(title),ln = True)
        
        line_y = self.get_y()
        self.set_draw_color(226, 232, 240)
        self.line(self.l_margin, line_y, self.w - self.r_margin, line_y)
        self.ln(2)
                
        #summary text 
        self.set_font("helvetica","",9.5)
        self.set_text_color(74,85,104)
        self.multi_cell(0,4.8,summary)
        self.ln(4)
        
        #Reset text color
        self.set_text_color(0,0,0)
        
    def side_graph_page(self,img_path,title, summary, w = 92,h = 58):
        """
        Places a graph plot on the left side and a clean technical summary description on the right.
        Args
        img_path(str):
            image path
        title(str):
            title for the graph
         summary(str)
         w(int) = 92:
             graph width
        h(int) = 58:
            graph height
        """
        self._check_page(h + 5)
        y = self.get_y()
        page_width = self.w - self.l_margin - self.r_margin
        
        if os.path.exists(img_path):
            self.image(img_path, x=self.l_margin, y= y, w= w, h= h)
        
        gap = 5
        text_x = self.l_margin + w + gap
        text_w = page_width - w - gap
        
        self.set_xy(text_x, y + 2)
        self.set_font("helvetica", "B", 10.5)
        self.set_text_color(26, 54, 93)
        self.cell(w, 5, str(title), ln=True)
        
        self.set_draw_color(226, 232, 240)
        self.line(text_x, y + 8, text_x + text_w, y + 8)
        
        self.set_xy(text_x, y + 10)
        self.set_font("helvetica", "", 9)
        self.set_text_color(74, 85, 104)
        self.multi_cell(text_w, 4.5,summary)
        
        self.set_text_color(0, 0, 0)
        self.set_y(y + h + 5)        

    def add_callout_box(self, title, text, box_height=20):
        """Creates a stylized soft-blue notification block for highlight metrics."""
        self._check_page(box_height + 5)
        w = self.w - self.l_margin - self.r_margin
        y = self.get_y()
        
        self.set_fill_color(235, 248, 255) 
        self.rect(self.l_margin, y, w, box_height, 'F')
        self.set_fill_color(49, 130, 206)  
        self.rect(self.l_margin, y, 1.5, box_height, 'F')
        
        self.set_xy(self.l_margin + 4, y + 2)
        self.set_font('helvetica', 'B', 9.5)
        self.set_text_color(44, 82, 130)
        self.cell(0, 4, title, 0, 1, 'L')
        
        self.set_xy(self.l_margin + 4, y + 7)
        self.set_font('helvetica', '', 8.5)
        self.set_text_color(45, 55, 72)
        self.multi_cell(w - 6, 4, text)
        
        self.set_text_color(0, 0, 0)
        self.set_xy(self.l_margin, y + box_height + 4)                
          
    #First Page    
    def cover_page(self,title,overview,df=None,author="Mpho",dataset ="Retail Dataset",github="https://github.com/Mpho048"):
        self.add_page()
        # Hero banner
        self.set_fill_color(*self.bg_color)
        self.set_text_color(255,255,255)
        
        self.set_font("helvetica","B",22)
        self.cell(0,18,title,fill=True,ln=True,align="C")
        self.set_text_color(0,0,0)
        self.ln(10)
        
        self.set_font("helvetica","B",12)
        self.cell(35,8,"Author:")
        
        self.set_font("helvetica","",12)
        self.cell(0,8,author,ln=True)
        
        self.set_font("helvetica","B",12)
        self.cell(35,8,"Dataset:")
        
        self.set_font("helvetica","",12)
        self.cell(0,8,dataset,ln=True)
        
        self.set_font("helvetica","B",12)
        self.cell(35,8,"Date:")
        
        self.set_font("helvetica","",12)
        self.cell(0,8,datetime.now().strftime("%d/%m/%Y"),ln=True)
        self.cell(35,8,"GitHub:")
        self.set_text_color(0,0,255)
        self.cell(0,8,github,ln=True,link=github)
        self.set_text_color(0,0,0)
        
        self.ln(8)
        self.set_fill_color(245,245,245)
        self.multi_cell(0,8,overview,border=1,fill=True)
        self.ln(5)
        self.write_txt("Dataset Preview:")
        self.create_table(df.head(6))          
    
    #Second Page
    def dataset_information(self,df):
        """ 
        Page 2,showing Dataset information
        Args:
        df(pd.DataFrame):
            The dataset
        """
        self.add_page()                 
        self.Set_title("Dataset Information") 
        size = round(df.memory_usage(deep=True).sum()/1024**2,2)
           
        metrics = [
        ("Rows",len(df)),
        ("Columns", len(df.columns)),
        ("Missing",df.isna().sum().sum()),
        ("Memory Usage",self._format_size(df)),
        ]
        self._metric_row(metrics)
        
        self._divider()
        
        info  = []
        for col in df.columns:
            all = (col,str(df[col].dtype),(df[col].isna().sum()))
            info.append(all)
            
        self.set_font("helvetica",size = 10)
        with self.table() as table:
            row = table.row()
            row.cell("Column")
            row.cell("Data Type")
            row.cell("Missing")
            
            for col,dtype,missing in info:
                row = table.row()
                row.cell(str(col))
                row.cell(str(dtype))
                row.cell(str(missing))
    
    #Insight page (5 or 6)
    def insights(self,findings,title = "Key Insights"):
        """ 
        Add insights page
        Args:
        findings(list or tuple):
            list or tuple
        title(str):
            page title
        """
        self.add_page()
        self.Set_title(title)
        self.set_fill_color(245,245,245)
        text = ""
               
        for i,item in enumerate(findings, 1):
            text += f"{i}. {item}\n\n"
        self.multi_cell(0,8,text,border = 1, fill = True)

        

#================================
#PDF tools
#================================


class PDFTool:
    """
    PDF utility class:
    - Extract tables
    - Extract multi-page tables
    - Extract table by area
    - Merge PDFs
    - Insert pages
    - Split PDFs
    """    
    def __init__(self,filepath = None) :
        self.filepath = None
        if filepath:
            self.filepath = self._valid_path(filepath)


    def _valid_path(self,path):
        """Validate path exists and is string.
        Args:
            path:str
        """
                
        if not isinstance(path,str):
            raise TypeError("Path must be a string(text)")
        if  not os.path.exists(path):
                raise FileNotFoundError(f"{path} does not exist")
        return path

    def update_filepath(self,new_path):
        """Input a new file path:
            Args:
                new_path(str)"""
        self.filepath = self._valid_path(new_path)

    def _check_file(self):
        """Ensure working file exists."""
        if self.filepath is None:
            raise ValueError("No PDF filepath selected")
              

    # --- pdfplumber TABLE EXTRACTION STRATEGIES ---
    def extract_table(self,page_num = 1):
        """Extracting table from pdf using tabula
        Args:
            page_num:(int / list)"""
        try:
            with plb.open(self.filepath) as f:
                page = f.pages[page_num-1]
                table = page.extract_table()
                return table if table else []
        except Exception as e:
            return f"Error: {e}"                                                                                
    def extract_multi_table(self,start_page,end_page):
        combine = []
        try:
            with plb.open(self.filepath) as f:
                for p_num in range(start_page-1, end_page):
                    page = f.pages[p_num]
                    table = page.extract_table()
                    if table is None:
                        continue
                    if not combine:
                        combine.extend(table)
                    else:
                        combine.extend(table[1:])
            return  combine                  
        except Exception as e:
            return f"Error {e}"                                                                                                     
    def extract_tables(self, page_num=1, table_num=None):
        """
        Extract all tables or one specific table
    
        Args:
            page_num : int
            table_num : int or None
    
        Returns:
            list
        """
    
        self._check_file()
    
        try:
            with plb.open(self.filepath) as f:    
                page = f.pages[page_num-1]    
                tables = page.extract_tables()
    
                if not tables:
                    return []    
                # Return one specific table
                if table_num is not None:
    
                    if table_num < 1:
                        raise ValueError("table_num starts at 1")
    
                    if table_num > len(tables):
                        raise IndexError("Table number out of range")
    
                    return tables[table_num-1]
    
                # Return all tables
                return tables
    
        except Exception as e:
            return f"Error: {e}"                                  
                                                            
    # --- MANIPULATION METHODS (pypdf) ---
    
    def merge_pdf(self,sec_pdf,output_name,pages= None):
        """
        Merge another PDF
        Args:
        output_name:str name of the new pdf       
        sec_pdf:str path/name of the second  pdf 
        pages:
            None -> all pages
            [1,2,4]  -> selected pages      
        """
        self._check_file()
        second_pdf = self._valid_path(sec_pdf)

        if not output_name.endswith("pdf"):
            output_name += ".pdf"

        writer = PdfWriter()
        reader1 = PdfReader(self.filepath)
        reader2 = PdfReader(second_pdf)
        

        for page in reader1.pages:
            writer.add_page(page)
            
        for index, page in enumerate(reader2.pages):

            if pages is not None:

                if index not in pages:
                    continue

            writer.add_page(page)

        with open(output_name,"wb") as f:
            writer.write(f)

        return output_name
                                                    
                        
                
    def insert_pdf(self,sec_pdf,page_num,insert_index,output_name):
        """
        Insert a page into the current pdf
        Args:
        sec_pdf(str):
            name of the second pdf,                         page_num(int):
           page number of the page to Insert,
        insert_index(int):
            new page number,
        output_name(str):
            name of the pdf
        """        
        self._check_file()
        second_pdf = self._valid_path(sec_pdf)
        
        if not output_name.endswith(".pdf"):
            output_name += ".pdf"
            
        reader1 = PdfReader(self.filepath)
        writer = PdfWriter()
        reader2 = PdfReader(second_pdf)
        page_num  -= 1
        insert_index  -= 1

        if page_num >= len(reader2.pages):
            raise IndexError("Page doesn't exist")

        if insert_index > len(reader1.pages):
            raise IndexError("Invalid insert index")                     

        for page in reader1.pages:
            writer.add_page(page)
            
        writer.insert_page(reader2.pages[page_num],(insert_index))
        
        with open(output_name,"wb") as f:
            writer.write(f)

        return output_name                                                                

    def _split_all(self,output):
        reader = PdfReader(self.filepath)
        
        for i,page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            filename = os.path.join(output,f"page_{i+1}.pdf")            
            with open(filename,"wb") as f:
                writer.write(f)
                 
    def split_pdf(self,output_dir = "SplitPdf",pages = "all"):
        self._check_file()
        os.makedirs(output_dir,exist_ok = True)
        
        if isinstance(pages,str) and pages.lower() == "all":
            self._split_all(output = output_dir)
            
        if isinstance(pages,list):
            reader = PdfReader(self.filepath)
            for i in pages:
                page =  i - 1
                writer = PdfWriter()
                writer.add_page(reader.pages[page])
                filename = os.path.join(output_dir,f"page_{i}.pdf")
                with open(filename,"wb") as f:
                    writer.write(f)
        if not isinstance(pages,(str,list)):
            return "pages has to be 'all' or a list of integers"          
            
        return f"Split completed in folder: '{output_dir}'"                                                                                     
 
#========SQLITE METHODS========

    #Save to sql(database)
    def df_to_sql(self,df,db_name="data.db",table_name="pdf_table", replace = False):
        """
        save dataframe into a sql database         Args
        df (pd.DataFrame):
            pandas dataframe
        db_name(str):
            name of the database
         table_name(str):
             name of the table to save to the                 database
         replace(bool):
             default  = False
        """
        self._valid_path(db_name)
        conn = sql.connect(db_name)
        
        mode = ("replace" if replace else "append")
        
        df.to_sql(table_name,conn,if_exists = mode,index = False)
        
        conn.close()
        return  "Saved successfully"
           
        
    #Read a table from database(to df)
    def sql_to_df(self,db_name,table_name):
        """"
        Read from sql database and get a table and turn it into dataframe
        Args:
        db_name(str):
            name of database
         table_name(str):
             name of the table in the database
        """
        self._valid_path(db_name)
        conn = sql.connect(db_name)
    
        try:
            query = (
            f"SELECT *"
            f"FROM [{table_name}]"
            )
            df = pd.read_sql(query,conn)
            return df
        finally:
            conn.close()
            
function addSelectLine() {
    let table = document.getElementById('search-table');
    let rowCount = table.rows.length;
    let cellCount = table.rows[rowCount-1].cells.length;
    let newRow = table.insertRow(rowCount);
    newRow.className="searchRow";

    let cell0 = document.createElement("select");
    cell0.className = "bool_select";
    cell0.add(new Option("AND","AND"));
    cell0.add(new Option("OR","OR"));
    cell0.add(new Option("NOT","NOT"));
    newRow.appendChild(cell0);

    let cell1 = document.createElement("input");
    cell1.type="text";
    cell1.className = "focusinput";
    cell1.colSpan = 1;
	//cell1.value=rowCount;
	newRow.id = rowCount;
    newRow.appendChild(cell1);

    let cell2 = document.createElement("select");
    cell2.className= "selectOption";
    cell2.add(new Option("Title","Title"));
    cell2.add(new Option("Keyword","Keyword"));
    cell2.add(new Option("Author","Author"));
    newRow.appendChild(cell2);

	let cell3 = table.rows[rowCount-1].cells[cellCount-1];
    newRow.appendChild(cell3);
}

function deleteSelectLine() {
    let table = document.getElementById('search-table');
    let rowCount = table.rows.length-1;
    //document.getElementById("output").value = rowCount;
    if(rowCount!=0){
        table.deleteRow(rowCount);
    }
}

function Search() {
    let table = document.getElementById("search-table");
    let rowCount = table.rows.length;
    var a = 1;

    text = document.getElementsByClassName("focusinput")
    for(var x=0;x<text.length;x++){
        if(text[x].value == null || text[x].value == ""){
             alert("Input can't be empty");
             a = 0;
             break;
        }
    }
    if(a==1){
        var temp = document.createElement("form");
        temp.action = "/search-result";
        temp.method="get";

        let name = document.getElementsByClassName("selectOption");
        let bool = document.getElementsByClassName("bool_select");


        for(var i=0;i<rowCount;i++){
            if(i==0){
                var opt = document.createElement("textarea");
                opt.name = "first";
                opt.value = name[i].value + " " + text[i].value;
                temp.appendChild(opt);
            }else{
                var opt = document.createElement("textarea");
                opt.name = name[i].value;
                opt.value = bool[i-1].value+" "+text[i].value+",";
                if(opt.name in temp){
                    opt.value = temp[opt.name].value +  opt.value;
                    temp[opt.name].value = opt.value
                }
                else {
                    temp.appendChild(opt);
                }
            }
        }
        temp.style.display="none"
        document.body.appendChild(temp);
        temp.submit();


        }
}

function apply() {
    var temp = document.createElement("form");
        temp.action = "/search-result";
        temp.method="get";
        var opt = document.createElement("textarea");
        opt.name = "date";
        opt.value = document.getElementById('date').value;
        temp.appendChild(opt);
        var opt1 = document.createElement("textarea");
        opt1.name = "cited";
        opt1.value = document.getElementById('cited').value;
        temp.appendChild(opt1);
        var opt2 = document.createElement("textarea");
        opt2.name = "search-condition";
        opt2.value = document.getElementById('searchCondition').innerText;
        temp.appendChild(opt2);
     if(opt.value=="100"&&opt1.value=="100"){
         alert("You can't select two 100%")
     }else{
        temp.style.display="none"
        document.body.appendChild(temp);
        temp.submit();
     }
}

function Second_search(){
    var start = document.getElementById("start").value;
    var end = document.getElementById("end").value;
    var data = null;
    if(document.getElementById("publisher1")!=null){
        data = document.getElementById("publisher1").value;
    }
    if(document.getElementById("IEEE").checked==true){
        data = "IEEE";
    }
    if(document.getElementById("ACM").checked==true){
        data = "ACM";
    }
    document.getElementById("start").value = start;
    document.getElementById("end").value = end;

     var temp = document.createElement("form");
     temp.action = "/search-result";
     temp.method="get";
     var opt = document.createElement("textarea");
     opt.name = "date";
     opt.value = document.getElementById('date').value;
     temp.appendChild(opt);
     var opt1 = document.createElement("textarea");
     opt1.name = "cited";
     opt1.value = document.getElementById('cited').value;
     temp.appendChild(opt1);
     var opt2 = document.createElement("textarea");
     opt2.name = "search-condition";
     opt2.value = document.getElementById('searchCondition').innerText;
     temp.appendChild(opt2);
     var opt3 = document.createElement("textarea");
     opt3.name = "start";
     opt3.value = start;
     temp.appendChild(opt3);
     var opt4 = document.createElement("textarea");
     opt4.name = "end";
     opt4.value = end;
     temp.appendChild(opt4);
     if(data!=null){
         var opt5 = document.createElement("textarea");
     opt5.name = "publisher";
     opt5.value = data;
     temp.appendChild(opt5);
     }

     temp.style.display="none";
     document.body.appendChild(temp);
     temp.submit();
}


function show(x) {
    var temp = document.createElement("form");
     temp.action = "/search-result";
     temp.method="get";

     if( document.getElementById('date1')!=null){
     var opt = document.createElement("textarea");
     opt.name = "date";
     opt.value = document.getElementById('date1').innerText;
     temp.appendChild(opt);
     var opt1 = document.createElement("textarea");
     opt1.name = "cited";
     opt1.value = document.getElementById('cited1').innerText;
     temp.appendChild(opt1);
     }
     var opt2 = document.createElement("textarea");
     opt2.name = "search-condition";
     opt2.value = document.getElementById('searchCondition').innerText;
     temp.appendChild(opt2);
     var opt3 = document.createElement("textarea");
     opt3.name = "currentpage";
     opt3.value = x;
     temp.appendChild(opt3);
     if(document.getElementById('start1')!=null){
         var opt4 = document.createElement("textarea");
        opt4.name = "start";
        opt4.value = document.getElementById('start1').innerText;
        temp.appendChild(opt4);
        var opt5 = document.createElement("textarea");
        opt5.name = "end";
        opt5.value = document.getElementById('end1').innerText;
        temp.appendChild(opt5);
     }
     if(document.getElementById('publisher1')!=null){
         var opt6 = document.createElement("textarea");
        opt6.name = "publisher";
        opt6.value = document.getElementById('publisher1').innerText;
        temp.appendChild(opt6);
     }
     //temp.appendChild(opt2);

     temp.style.display="none";
     document.body.appendChild(temp);
     temp.submit();
}

function original() {
    var temp = document.createElement("form");
     temp.action = "/search-result";
     temp.method="get";
    var opt2 = document.createElement("textarea");
     opt2.name = "search-condition";
     opt2.value = document.getElementById('searchCondition').innerText;
     temp.appendChild(opt2);
     temp.style.display="none";
     document.body.appendChild(temp);
     temp.submit();
}
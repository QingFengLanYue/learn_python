package test;

public class JpypeDemo {

    public static String sayHello(String user){ //注意！作为被 python调用的接口函数，需要是静态的，否则 python 端会报错
        return "hello " + user;
    }
    public static int calc(int a, int b){  //注意！作为被 python 调用的接口函数，需要是静态的，否则 python 端会报错
        return a + b;
    }
    public static void main(String[] args){
        int a = 10;
        int b = 12;
        JpypeDemo x = new JpypeDemo();

        System.out.println(x.calc(a,b));
        String user = "xiaoming";
        System.out.println(x.sayHello(user));


    }
}
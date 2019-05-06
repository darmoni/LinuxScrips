/*
 * std::thread Threading with c++17
 * Soutce: https://en.cppreference.com/w/cpp/thread/thread/thread

 $Id$ $Date$

*/
#include <iostream>
#include <utility>
#include <thread>
#include <chrono>
#include <vector>
#include <map>
#include <string>
#include <mutex>
#include <shared_mutex>

void f1(int n)
{
    std::thread::id id = std::this_thread::get_id();
    for (int i = 0; i < 5; ++i) {
        ++n;
        std::cout << "Thread 1 executing, n = " << n << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    std::cout << "Thread 1 id = " << id << "\n";
}

void f2(int& n)
{
    for (int i = 0; i < 5; ++i) {
        ++n;
        std::cout << "Thread 2 executing, n = " << n << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

class foo
{
public:
    void bar()
    {
        for (int i = 0; i < 5; ++i) {
            ++n;
            std::cout << "Thread 3 executing, n = " << n << "\n";
            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
        std::cout << "Thread 3 Done\n";
    }
    int n = 0;
};

template<class T>
class protect
{
    T protectee;
    mutable std::shared_mutex protectee_mutex;

public:
    protect(T value):protectee(value)
    {
    }
    T get(void) const   // safe read
    {
        std::shared_lock reader(protectee_mutex);
        return protectee; // by value
    }
    T add (T modifier) {
        std::unique_lock writer(protectee_mutex);
        protectee += modifier; // by value
        //std::cout << "*protect() = " << protectee << " \n";
        return protectee;
    }
    T operator *(void) const   // safe read
    {
        return get();
    }
    T operator +=(T modifier)    // safe write
    {
        return add(modifier);
    }

};


std::map<std::string, std::string> g_pages;
std::mutex g_pages_mutex;

void save_page(const std::string &url)
{
    // simulate a long page fetch
    std::this_thread::sleep_for(std::chrono::seconds(2));
    std::string result = "fake content";

    std::lock_guard<std::mutex> guard(g_pages_mutex);
    g_pages[url] = result;
}

struct Employee {
    Employee(std::string id) : id(id) {}
    std::string id;
    std::vector<std::string> lunch_partners;
    std::mutex m;
    std::string output() const
    {
        std::string ret = "Employee " + id + " has lunch partners: ";
        for( const auto& partner : lunch_partners )
            ret += partner + " ";
        return ret;
    }
};

void send_mail(Employee &, Employee &)
{
    // simulate a time-consuming messaging operation
    std::this_thread::sleep_for(std::chrono::seconds(1));
}

void assign_lunch_partner(Employee &e1, Employee &e2)
{
    static std::mutex io_mutex;
    {
        std::lock_guard<std::mutex> lk(io_mutex);
        std::cout << e1.id << " and " << e2.id << " are waiting for locks" << std::endl;
    }

    {
        // use std::scoped_lock to acquire two locks without worrying about
        // other calls to assign_lunch_partner deadlocking us
        // and it also provides a convenient RAII-style mechanism

        std::scoped_lock lock(e1.m, e2.m);

        // Equivalent code 1 (using std::lock and std::lock_guard)
        // std::lock(e1.m, e2.m);
        // std::lock_guard<std::mutex> lk1(e1.m, std::adopt_lock);
        // std::lock_guard<std::mutex> lk2(e2.m, std::adopt_lock);

        // Equivalent code 2 (if unique_locks are needed, e.g. for condition variables)
        // std::unique_lock<std::mutex> lk1(e1.m, std::defer_lock);
        // std::unique_lock<std::mutex> lk2(e2.m, std::defer_lock);
        // std::lock(lk1, lk2);
        {
            std::lock_guard<std::mutex> lk(io_mutex);
            std::cout << e1.id << " and " << e2.id << " got locks" << std::endl;
        }
        e1.lunch_partners.push_back(e2.id);
        e2.lunch_partners.push_back(e1.id);
    }

    send_mail(e1, e2);
    send_mail(e2, e1);
}

int main()
{

    Employee alice("alice"), bob("bob"), christina("christina"), dave("dave");

    // assign in parallel threads because mailing users about lunch assignments
    // takes a long time
    std::vector<std::thread> threads;
    threads.emplace_back(assign_lunch_partner, std::ref(alice), std::ref(bob));
    threads.emplace_back(assign_lunch_partner, std::ref(christina), std::ref(bob));
    threads.emplace_back(assign_lunch_partner, std::ref(christina), std::ref(alice));
    threads.emplace_back(assign_lunch_partner, std::ref(dave), std::ref(bob));


    std::thread t01(save_page, "http://foo");
    std::thread t02(save_page, "http://bar");

    int n = 0;
    foo f;
    std::thread t1; // t1 is not a thread
    std::thread t2(f1, n + 1); // pass by value
    std::thread t3(f2, std::ref(n)); // pass by reference
    std::thread t4(std::move(t3)); // t4 is now running f2(). t3 is no longer a thread
    std::thread t5(&foo::bar, &f); // t5 runs foo::bar() on object f

    t4.join();
    t5.join();
    t2.join();

    protect<std::string> strProtectee("readOnly");
    protect<int> IntProtectee(2019);

    auto add_and_print = [&IntProtectee]() {
        for (int i = 1; i < 4; i++) {
            IntProtectee.add(i);
            std::cout << __LINE__ << ' '<< std::this_thread::get_id() << ' ' << IntProtectee.get() << '\n';

            // Note: Writing to std::cout actually needs to be synchronized as well
            // by another std::mutex. This has been omitted to keep the example small.
        }
    };
    std::cout << __LINE__ << " main()  " << IntProtectee.get() << '\n';
    std::thread thread1(add_and_print);
    std::cout << __LINE__ << " main()  " << IntProtectee.get() << '\n';
    std::thread thread2(add_and_print);
    std::cout << __LINE__ << " main()  " << IntProtectee.get() << '\n';

    std::cout << "*protect() = " << *strProtectee << " \n";
    strProtectee += ".";
    strProtectee += "NowWritten";
    std::cout << "*protect() = " << *strProtectee << " \n";

    std::cout << "Final value of n is " << n << '\n';
    std::cout << "Final value of foo::n is " << f.n << '\n';

    t01.join();
    t02.join();
    // safe to access g_pages without lock now, as the threads are joined
    for (const auto &pair : g_pages) {
        std::cout << pair.first << " => " << pair.second << '\n';
    }
    thread1.join();
    thread2.join();
    std::cout << __LINE__ << " main()  " << IntProtectee.get() << '\n';

    for (auto &thread : threads) thread.join();
    std::cout << alice.output() << '\n'  << bob.output() << '\n'
    << christina.output() << '\n' << dave.output() << '\n';

}
